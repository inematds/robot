#!/usr/bin/env python3
"""Catálogo PT (docs/) → i18n/source.json (offline). Chave = sha256(texto normalizado)[:16].
Código: <code> em linha não traduz; <pre> traduz só comentários/strings (translate.py confere).
Uso: python3 scripts/localization.py"""
from pathlib import Path
from bs4 import BeautifulSoup, Comment, Doctype
import json, re, hashlib

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / 'docs'
I18N = REPO / 'i18n'
ATTRS = ('aria-label', 'title', 'alt', 'placeholder')
SKIP = {'INEMA.CLUB', 'PRO', 'PT', 'EN', 'ES', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'ESP32', 'ESP32-S3', 'Arduino',
        'Raspberry Pi', 'Raspberry Pi 5', 'ROS 2', 'LeRobot', 'SO-101', 'YOLO26', 'Nav2', 'OpenCV', 'Wokwi',
        'GitHub', 'MIT', 'micro-ROS', 'Gazebo', 'LiDAR', 'PID', 'IMU', 'BLE', 'Wi-Fi', 'GND', 'VCC', 'PWM', 'GPIO'}


def norm(s):
    return re.sub(r'\s+', ' ', str(s)).strip()


def ident(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def pages():
    man = json.loads((ROOT / 'curso/_shared/manifest.json').read_text())
    out = [ROOT / 'index.html']
    for tr in man['tracks']:
        out.append(ROOT / f"curso/trilha{tr['n']}/index.html")
        out += [ROOT / m['href'] for m in tr['modules']]
    return [p for p in out if p.exists()]


def eligible(s):
    return bool(re.search(r'[A-Za-zÀ-ÿ]{2}', s)) and s not in SKIP


def pre_has_human_text(s):
    """Pedaço de bloco de código que tem algo para traduzir: comentário, string com palavras, ou prosa."""
    if not re.search(r'[A-Za-zÀ-ÿ]{3}', s):
        return False
    if re.search(r'(//|/\*|<!--|(^|\s)#(?!include|define|if|endif|else|pragma|!))\s*\S', s):
        return True
    if re.search(r'["\'][^"\'\n]*[A-Za-zÀ-ÿ]{3}[^"\'\n]*\s[^"\'\n]*["\']', s):
        return True
    if re.search(r'[áàâãéêíóôõúçÁÉÍÓÚÇ]', s):
        return True
    code = len(re.findall(r'[;(){}=<>\[\]_]', s))
    words = len(re.findall(r'[A-Za-zÀ-ÿ]{3,}', s))
    return words >= 6 and code / max(1, len(s)) < 0.02


def text_nodes(soup):
    for n in soup.find_all(string=True):
        if isinstance(n, (Comment, Doctype)) or n.parent.name in ('script', 'style', 'noscript'):
            continue
        if n.find_parent(class_='inema-lang') or n.find_parent(attrs={'translate': 'no'}):
            continue
        if n.find_parent('code') and not n.find_parent('pre'):
            continue
        if n.find_parent('pre') and not pre_has_human_text(str(n)):
            continue
        if eligible(norm(n)):
            yield n


def kind(n):
    return 'pre' if n.find_parent('pre') else 'text'


def key_of(s, k='text'):
    v = norm(s) if k == 'text' else s
    return (ident(v), v) if eligible(norm(v)) else (None, v)


def meta_targets(soup):
    return [t for t in soup.find_all('meta') if t.get('name') == 'description' or t.get('property') in ('og:title', 'og:description')]


def catalog():
    out = {}

    def add(s, k='text'):
        h, v = key_of(s, k)
        if h:
            out[h] = {'source': v, 'kind': k}

    for path in pages():
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        for n in text_nodes(soup):
            add(str(n), kind(n))
        for tag in soup.find_all(True):
            for a in ATTRS:
                if tag.get(a):
                    add(tag[a])
        for t in meta_targets(soup):
            add(t['content'])
        if soup.title:
            add(soup.title.get_text())
        m = soup.select_one('[data-inema-manifest]')
        if m:
            for tr in json.loads(m.string)['tracks']:
                add(tr['title'])
                for mo in tr['modules']:
                    add(mo['title'])
    return out


if __name__ == '__main__':
    I18N.mkdir(exist_ok=True)
    out = catalog()
    (I18N / 'source.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(len(out), 'segmentos;', sum(len(v['source']) for v in out.values()), 'caracteres;',
          sum(1 for v in out.values() if v['kind'] == 'pre'), 'blocos de código')
