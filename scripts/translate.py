#!/usr/bin/env python3
"""Traduz i18n/source.json → i18n/<lang>.json (cache incremental). Só o tradutor central do INEMA
(inema-traduz, INEMA_TRADUCAO_* em ~/.config/inema/modelos.env, hoje Sonnet 5.5) pela assinatura. Sem API. Uso: python3 scripts/translate.py en es [--jobs 4]"""
import json, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
I18N = REPO / 'i18n'
NAME = {'en': 'clear, natural English (global audience)', 'es': 'neutral Latin American Spanish'}
SYSTEM = """You are a careful professional translator of an educational ROBOTICS course (Arduino/ESP32, Raspberry Pi, computer vision, ROS 2, LeRobot) from Brazilian Portuguese into {name}.
Translate ALL provided content. Do not summarize, omit or add. Return ONLY a JSON object mapping each exact input ID to the translated string (no other keys).
Rules:
- Keep product, library, model, command, function, file, pin and variable names EXACTLY (ESP32, ledcAttach, ROS 2, Nav2, slam_toolbox, YOLO26, LeRobot, SO-101, INEMA.CLUB, Wokwi, GPIO 2, etc.). Never translate inside URLs or paths.
- Fragments may start/end mid-sentence (inline markup was split): translate only the fragment, keep leading/trailing punctuation and spacing.
- Items with kind "pre" are CODE BLOCKS (C++/Arduino, Python, shell, YAML, URDF/XML). Keep EVERY character of the code identical, including identifiers, numbers, indentation and newlines. Translate ONLY the human-language parts: comments (after //, #, inside /* */ or <!-- -->) and the text inside string literals that is shown to a person (e.g. Serial.println("Distância: ") → "Distance: "). Do not translate format specifiers, topic names, file names or JSON keys.
- Keep numbers, units (V, mA, Ω, cm), prices in R$ and dates unchanged.
- Brazilian references (OBR, BNCC, Brazilian stores) stay as names; you may keep them as is.
- Use a friendly, direct second person ("you"/"tú"), no hype."""


_TRADUTOR = os.path.expanduser("~/projetos/wifi/scripts/inema-traduz")
def chamar_tradutor(pedido: str, timeout: int = 900) -> str:
    """Tradução pelo tradutor central do INEMA (INEMA_TRADUCAO_* em ~/.config/inema/modelos.env). Assinatura, nunca API."""
    if os.path.exists(_TRADUTOR):
        cmd = [_TRADUTOR]
    else:  # fora da máquina do Nei: Claude Code da assinatura com o modelo da variável (padrão Sonnet 5.5)
        cmd = ["claude", "-p", "--model", os.environ.get("INEMA_TRADUCAO_MODELO", "claude-sonnet-5-5"),
               "--output-format", "text", "--tools", ""]
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "CLAUDECODE")}
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run(cmd, input=pedido, capture_output=True, text=True, timeout=timeout, env=env, cwd=d)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(f"tradutor falhou rc={r.returncode}: {(r.stderr or r.stdout)[-300:]}")
    return r.stdout


def tradutor_json(system, payload):
    t = chamar_tradutor(system + '\n\nReturn ONLY the JSON object (no code fences).\nINPUT JSON:\n' + payload, timeout=1200)
    t = re.sub(r'^```(?:json)?\s*|\s*```$', '', t.strip())
    return json.loads(t[t.index('{'):t.rindex('}') + 1])


def code_skeleton(s):
    """Remove comentários e strings; o que sobra (código) tem que ficar idêntico."""
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    s = re.sub(r'"(?:\\.|[^"\\\n])*"', '""', s)
    s = re.sub(r"'(?:\\.|[^'\\\n])*'", "''", s)
    s = re.sub(r'(//|#).*', '', s)
    return re.sub(r'\s+', '', s)


def check(batch, raw):
    if set(raw) != set(batch):
        raise ValueError(f'IDs divergentes: faltam {len(set(batch) - set(raw))}')
    bad = []
    for k, v in raw.items():
        src = batch[k]
        if not isinstance(v, str) or not v.strip():
            bad.append(k); continue
        if len(src['source']) > 200 and len(v) < len(src['source']) * .45:
            bad.append(k); continue
        if src['kind'] == 'pre' and code_skeleton(v) != code_skeleton(src['source']):
            bad.append(k); continue
    return bad


def batches(missing, limit=5000):
    out, cur, size = [], {}, 0
    for k, v in missing:
        if size + len(v['source']) > limit and cur:
            out.append(cur); cur, size = {}, 0
        cur[k] = v; size += len(v['source'])
    if cur:
        out.append(cur)
    return out


def run(lang, jobs):
    src = json.loads((I18N / 'source.json').read_text())
    path = I18N / f'{lang}.json'
    cache = json.loads(path.read_text()) if path.exists() else {}
    rejects_path = I18N / f'{lang}.rejects.json'
    missing = [(k, v) for k, v in src.items() if k not in cache]
    todo = batches(missing)
    print(lang, len(missing), 'faltando em', len(todo), 'lotes', flush=True)
    system = SYSTEM.format(name=NAME[lang])
    rejects = {}

    def work(i_b):
        i, b = i_b
        for tent in range(4):
            try:
                ids = {str(n): k for n, k in enumerate(b)}
                payload = json.dumps({n: b[k] for n, k in ids.items()}, ensure_ascii=False)
                raw = tradutor_json(system, payload)
                raw = {ids[n]: v for n, v in raw.items() if n in ids}
                # às vezes o modelo devolve o objeto de entrada com a tradução em "source"
                raw = {k: (v.get('source') if isinstance(v, dict) else v) for k, v in raw.items()}
                if set(raw) != set(b):
                    raise ValueError('IDs divergentes')
                bad = check(b, raw)
                good = {k: v for k, v in raw.items() if k not in bad}
                return i, good, {k: raw.get(k) for k in bad}
            except Exception as e:
                print(lang, 'lote', i, 'tentativa', tent + 1, 'falhou:', str(e)[:150], flush=True)
        return i, {}, {k: None for k in b}

    with ThreadPoolExecutor(jobs) as ex:
        for i, good, bad in ex.map(work, enumerate(todo, 1)):
            cache.update(good)
            rejects.update(bad)
            path.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
            print(lang, 'lote', i, '/', len(todo), 'ok', len(good), 'rejeitados', len(bad), 'cache', len(cache), flush=True)
    rejects_path.write_text(json.dumps(rejects, ensure_ascii=False, indent=2) + '\n')
    left = sum(1 for k in src if k not in cache)
    print(lang, 'FIM: faltam', left, flush=True)
    return left


if __name__ == '__main__':
    args = sys.argv[1:]
    jobs = 4
    if '--jobs' in args:
        i = args.index('--jobs'); jobs = int(args[i + 1]); del args[i:i + 2]
    left = sum(run(l, jobs) for l in (args or ['en', 'es']))
    print('ORQUESTRA_FIM faltam', left)
    sys.exit(1 if left else 0)
