#!/usr/bin/env python3
"""Extrai os code boxes das páginas PT e verifica:
- .ino  → arduino-cli compile (esp32:esp32:esp32, ou esp32s3 se o código citar S3/câmera/TFLite)
- .py   → compilação de sintaxe (py_compile)
Uso: python3 scripts/compile-check.py [filtro-de-arquivo]   (ex.: modulo-1-6)
Saída: OK/FALHA por bloco; rc=1 se algum falhar. Pula blocos com <partes variáveis> marcadas."""
import html, json, re, subprocess, sys, tempfile, py_compile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / 'docs'
ACLI = str(Path.home() / '.local/bin/arduino-cli')
filt = sys.argv[1] if len(sys.argv) > 1 else ''
man = json.loads((DOCS / 'curso/_shared/manifest.json').read_text())
pages = [DOCS / m['href'] for t in man['tracks'] for m in t['modules']]
BOX = re.compile(r'<span class="code-file">([^<]+)</span>.*?<pre[^>]*>(.*?)</pre>', re.S)
fails, oks, skips = [], 0, []
work = Path(tempfile.mkdtemp(prefix='robot-cc-'))

for p in pages:
    if filt not in str(p) or not p.exists():
        continue
    t = p.read_text()
    boxes = BOX.findall(t)
    # arquivos auxiliares (.h/.cpp) do mesmo módulo entram junto em todo sketch que os inclui
    extras = {Path(n.strip()).name: html.unescape(re.sub(r'<[^>]+>', '', b))
              for n, b in boxes if re.search(r'\.(h|hpp|cpp)$', n.strip())}
    for i, (name, body) in enumerate(boxes, 1):
        name = name.strip()
        code = html.unescape(re.sub(r'<[^>]+>', '', body))
        tag = f'{p.stem}#{i} {name}'
        if re.search(r'<(seu|sua|modelo|distro|isto)[^>]*>', code) and not name.endswith('.ino'):
            skips.append(tag); continue
        if name.endswith('.ino'):
            if re.search(r'<seu_projeto[^>]*_inferencing\.h>|_inferencing\.h', code):
                skips.append(tag + ' (Edge Impulse gerado)'); continue
            d = work / f'{p.stem}_{i}' / Path(name).stem
            d.mkdir(parents=True, exist_ok=True)
            (d / (Path(name).stem + '.ino')).write_text(code)
            for en, ec in extras.items():
                (d / en).write_text(ec)
            fqbn = 'esp32:esp32:esp32s3' if re.search(r'S3|esp_camera|TFLite|tflite|PSRAM', code) else 'esp32:esp32:esp32'
            if re.search(r'micro_ros|rcl/rcl\.h', code):
                skips.append(tag + ' (micro-ROS: lib externa)'); continue
            r = subprocess.run([ACLI, 'compile', '--fqbn', fqbn, str(d)], capture_output=True, text=True, timeout=600)
            if r.returncode:
                err = [l for l in (r.stdout + r.stderr).splitlines() if 'error' in l.lower()][:4]
                fails.append(f'{tag} [{fqbn}]: ' + ' | '.join(err)[:600])
            else:
                oks += 1
        elif name.endswith('.py'):
            f = work / f'{p.stem}_{i}.py'
            f.write_text(code)
            try:
                py_compile.compile(str(f), doraise=True); oks += 1
            except py_compile.PyCompileError as e:
                fails.append(f'{tag}: {str(e)[:300]}')
        elif re.search(r'\.(h|hpp|cpp)$', name):
            pass  # compilado junto com o .ino do módulo
        else:
            skips.append(tag)

for f in fails:
    print('FALHA', f)
print(f'== OK {oks} · FALHA {len(fails)} · pulados {len(skips)}')
if '-v' in sys.argv:
    print('pulados:', *skips, sep='\n  ')
sys.exit(1 if fails else 0)
