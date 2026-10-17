#!/usr/bin/env python3
"""Valida o curso v2 em docs/ (PT) ou docs/<lang>/. Uso: python3 scripts/validate.py [pt|en|es]
Saída: lista de problemas; rc=1 se houver algum."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'docs'
lang = sys.argv[1] if len(sys.argv) > 1 else 'pt'
base = ROOT if lang == 'pt' else ROOT / lang
man = json.loads((ROOT / 'curso/_shared/manifest.json').read_text())
FORBID = [r'ledcSetup', r'ledcAttachPin', r'\bGMapping\b', r'\bgmapping\b', r'raspistill', r'YOLOv5',
          r'Jetson Nano(?! Super)(?!.{0,40}(descontinu|discontinu|saiu de linha))', r'\bTODO\b', r'lorem ipsum',
          r'\[Nome', r'\[Resultado', r'\b\d+\s*(horas|hours)\b', r'\b\d+h\b(?![a-z])']
probs = []

def page_list():
    pages = [base / 'index.html']
    for tr in man['tracks']:
        pages.append(base / f"curso/trilha{tr['n']}/index.html")
        for m in tr['modules']:
            pages.append(base / m['href'])
    return pages

def strip_code(t):
    return re.sub(r'<(script|style)[^>]*>.*?</\1>', '', t, flags=re.S)

man_txt = json.dumps(man, sort_keys=True)
for p in page_list():
    rel = p.relative_to(ROOT)
    if not p.exists():
        probs.append(f'FALTA {rel}'); continue
    t = p.read_text()
    if not re.search(r'<meta (?=[^>]*name="inema-course")(?=[^>]*content="robot")[^>]*>', t):
        probs.append(f'{rel}: sem meta inema-course')
    m = re.search(r'<script (?=[^>]*type="application/json")(?=[^>]*data-inema-manifest)[^>]*>(.*?)</script>', t, re.S)
    if not m:
        probs.append(f'{rel}: sem manifesto')
    elif lang == 'pt' and json.dumps(json.loads(m.group(1)), sort_keys=True) != man_txt:
        probs.append(f'{rel}: manifesto diferente do _shared')
    if t.find('localStorage.getItem(\'inema.prefs\')') > t.find('cdn.tailwindcss.com') >= 0:
        probs.append(f'{rel}: anti-FOUC depois do Tailwind')
    if 'Sora' not in t:
        probs.append(f'{rel}: sem fonte Sora')
    if 'inema.pro' not in t:
        probs.append(f'{rel}: sem link PRO')
    vis = strip_code(t)
    for f in FORBID:
        for mm in re.finditer(f, vis):
            ctx = vis[max(0, mm.start()-60):mm.end()+40].replace('\n', ' ')
            probs.append(f'{rel}: proibido /{f}/ … {ctx[:140]}')
            break
    want_lang = {'pt': 'pt-BR', 'en': 'en', 'es': 'es'}[lang]
    if not re.search(rf'<html [^>]*lang="{want_lang}"', t):
        probs.append(f'{rel}: <html lang> != {want_lang}')

for tr in man['tracks']:
    for mo in tr['modules']:
        p = base / mo['href']
        if not p.exists():
            continue
        t = p.read_text()
        ids = re.findall(r'data-inema-topic="modulo-%s#topico-(\d+)"' % mo['id'], t)
        if sorted(set(ids), key=int) != [str(i) for i in range(1, mo['topics'] + 1)]:
            probs.append(f"{mo['href']}: tópicos {sorted(set(ids), key=int)} != 1..{mo['topics']}")
        n_svg = len(re.findall(r'<svg[^>]*role="img"', t))
        if n_svg < 3:
            probs.append(f"{mo['href']}: só {n_svg} SVG role=img (mín. 3)")
        lines = t.count('\n')
        if lines < 450:
            probs.append(f"{mo['href']}: {lines} linhas (mín. ~500)")
        if f'data-inema-module="{mo["id"]}"' not in t:
            probs.append(f"{mo['href']}: sem data-inema-module")

for p in probs:
    print(p)
print(f'== {len(probs)} problema(s) [{lang}]')
sys.exit(1 if probs else 0)
