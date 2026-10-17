#!/usr/bin/env python3
"""Gera docs/en/ e docs/es/ a partir do PT + i18n/<lang>.json (offline, sem API).
Regrava seletor de idioma e alternates no PT. Trecho sem tradução = erro (lista e sai rc=1).
Uso: python3 scripts/render-locales.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from localization import *
from bs4 import NavigableString
import posixpath

BASE = 'https://inematds.github.io/robot/'
LANGS = {'pt': 'pt-BR', 'en': 'en', 'es': 'es'}
COURSE_PAGES = {p.relative_to(ROOT).as_posix() for p in pages()}
SEL_STYLE = ('position:fixed;right:14px;bottom:14px;z-index:9999;display:flex;gap:2px;padding:4px;border-radius:10px;'
             'background:rgba(12,12,16,.85);border:1px solid rgba(250,204,21,.45);font:600 12px/1 Sora,Inter,system-ui,sans-serif;'
             'backdrop-filter:blur(8px)')
A_ON = 'padding:6px 8px;border-radius:7px;text-decoration:none;color:#1a1206;background:#FACC15'
A_OFF = 'padding:6px 8px;border-radius:7px;text-decoration:none;color:#e6e6e6'


def url_rel(rel):
    return '' if rel == 'index.html' else rel


def lang_ui(soup, rel, lang):
    for old in soup.select('.inema-lang,link[rel="canonical"],link[rel="alternate"][hreflang]'):
        old.decompose()
    pre = '' if lang == 'pt' else lang + '/'
    for code, loc in LANGS.items():
        p = '' if code == 'pt' else code + '/'
        soup.head.append(soup.new_tag('link', rel='alternate', hreflang=loc, href=BASE + p + url_rel(rel)))
    soup.head.append(soup.new_tag('link', rel='alternate', hreflang='x-default', href=BASE + url_rel(rel)))
    soup.head.append(soup.new_tag('link', rel='canonical', href=BASE + pre + url_rel(rel)))
    div = soup.new_tag('div', attrs={'class': 'inema-lang', 'style': SEL_STYLE, 'translate': 'no', 'aria-label': 'Idioma / Language'})
    here = posixpath.dirname(pre + rel)
    for code, loc in LANGS.items():
        tgt = ('' if code == 'pt' else code + '/') + rel
        href = posixpath.relpath(tgt, here or '.')
        if href.endswith('index.html') and rel == 'index.html':
            href = href[:-len('index.html')] or './'
        a = soup.new_tag('a', href=href, hreflang=loc, style=A_ON if code == lang else A_OFF)
        a.string = code.upper()
        div.append(a)
    soup.body.insert(0, div)


def fix_paths(soup, rel):
    """Página traduzida fica 1 nível abaixo: links para fora do curso (assets/, v1/, imagens) ganham ../"""
    here = posixpath.dirname(rel)
    for tag in soup.find_all(True):
        for attr in ('href', 'src'):
            v = tag.get(attr)
            if not v or re.match(r'^(?:[a-z]+:|#|//|data:)', v):
                continue
            path = v.split('#', 1)[0]
            if not path:
                continue
            tgt = posixpath.normpath(posixpath.join(here, path))
            if tgt in COURSE_PAGES or (tgt.rstrip('/') + '/index.html').lstrip('./') in COURSE_PAGES:
                continue
            tag[attr] = '../' + v


def render(lang):
    cache = json.loads((I18N / f'{lang}.json').read_text())
    missing = []

    def tr(s, k='text'):
        h, v = key_of(s, k)
        if not h:
            return s
        if h not in cache:
            missing.append(v[:80]); return s
        out = cache[h]
        if k == 'text':
            out = (' ' if s[:1].isspace() else '') + out + (' ' if s[-1:].isspace() else '')
        return out

    for path in pages():
        rel = path.relative_to(ROOT).as_posix()
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        for n in list(text_nodes(soup)):
            n.replace_with(NavigableString(tr(str(n), kind(n))))
        for tag in soup.find_all(True):
            for a in ATTRS:
                if tag.get(a):
                    tag[a] = tr(tag[a]).strip()
        for t in meta_targets(soup):
            t['content'] = tr(t['content']).strip()
        soup.html['lang'] = LANGS[lang]
        m = soup.select_one('[data-inema-manifest]')
        if m:
            man = json.loads(m.string)
            for t in man['tracks']:
                t['title'] = tr(t['title']).strip()
                for mo in t['modules']:
                    mo['title'] = tr(mo['title']).strip()
            m.string = '\n' + json.dumps(man, ensure_ascii=False, indent=2) + '\n'
        fix_paths(soup, rel)
        lang_ui(soup, rel, lang)
        out = ROOT / lang / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(str(soup))
    if missing:
        print(f'{lang}: {len(missing)} trechos sem tradução, ex.: {missing[:5]}')
        return False
    print(lang, ':', len(pages()), 'páginas')
    return True


if __name__ == '__main__':
    ok = all([render(l) for l in ('en', 'es')])
    for path in pages():
        rel = path.relative_to(ROOT).as_posix()
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        lang_ui(soup, rel, 'pt')
        path.write_text(str(soup))
    print('pt: seletor e alternates regravados')
    sys.exit(0 if ok else 1)
