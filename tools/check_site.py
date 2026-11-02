#!/usr/bin/env python3
"""Dependency-free structural, route and owner-constraint checks for this site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack = []
        self.ids = set()
        self.refs = []
        self.errors = []
        self.editorial_depth = None
        self.editorial = []
        self.main_count = 0
        self.h1_count = 0
        self.images = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'main': self.main_count += 1
        if tag == 'h1': self.h1_count += 1
        if 'id' in attrs:
            if attrs['id'] in self.ids: self.errors.append('duplicate id: '+attrs['id'])
            self.ids.add(attrs['id'])
        for key in ('href', 'src', 'poster'):
            if attrs.get(key): self.refs.append(attrs[key])
        if tag == 'img':
            self.images += 1
            if 'alt' not in attrs: self.errors.append('image without alt')
        if tag not in VOID:
            self.stack.append(tag)
            if 'data-editorial' in attrs: self.editorial_depth = len(self.stack)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append('unexpected closing tag: '+tag)
        else:
            if self.editorial_depth == len(self.stack): self.editorial_depth = None
            self.stack.pop()

    def handle_data(self, data):
        if self.editorial_depth: self.editorial.append(data)


def check():
    errors = []
    pages = {}
    for path in [*ROOT.glob('*.html'), *ROOT.glob('projects/*.html')]:
        if not path.stat().st_size:
            assert path.name == 'about.html', 'Unexpected empty page'
            continue
        page = Page(path)
        page.feed(path.read_text())
        pages[path.resolve()] = page
        if page.stack: page.errors.append('unclosed tags: '+str(page.stack))
        if page.main_count != 1 or page.h1_count != 1: page.errors.append('expected one main and h1')
        errors += [f'{path.relative_to(ROOT)}: {e}' for e in page.errors]
    checked = 0
    for path, page in pages.items():
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc: continue
            checked += 1
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_file(): errors.append(f'{path.relative_to(ROOT)}: missing {ref}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(ROOT)}: missing fragment {ref}')
        if path.name.endswith('-overview.html'):
            words = len(' '.join(page.editorial).split())
            assert 350 <= words <= 500, (path, words)
            assert 1 <= page.images <= 3
            print(f'{path.name}: {words} editorial words, {page.images} images')
    for css in ROOT.glob('css/*.css'):
        for ref in re.findall(r'url\([\"\']?([^\)\"\']+)', css.read_text()):
            if not urlsplit(ref).scheme and not (css.parent/ref).is_file(): errors.append(f'{css}: missing {ref}')
    assert not (ROOT/'projects/aircraft-design.html').exists()
    for path in [*ROOT.glob('*.html'), *ROOT.glob('projects/*.html'), *ROOT.glob('js/*.js'), *ROOT.glob('css/*.css')]:
        assert 'aircraft-design.html' not in path.read_text(), path
    uas = (ROOT/'projects/uas.html').read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(uas)).encode()+b'\0'+uas).hexdigest()
    assert blob == '8bc70dd14e66c34681a6db7aea5361f7e30175de', 'UAS was modified'
    home = (ROOT/'index.html').read_text()
    assert len(re.findall(r'<section\b', home)) == 4
    cv = (ROOT/'cv.html').read_text()
    assert re.findall(r'<h2[^>]*>(.*?)</h2>', cv) == ['Profile', 'Technical Skills', 'Professional Experience', 'Engineering Projects', 'Education', 'Additional Information']
    assert 'linus.adzankuu@gmail.com' in home and 'linus.adzankuu@gmail.com' in cv
    listing = (ROOT/'projects.html').read_text()
    assert listing.index('href="projects/aeroacoustics-overview.html"') < listing.index('href="projects/rocket-engine-overview.html"') < listing.index('href="projects/uas.html"')
    content = json.loads((ROOT/'tools/cv-content.json').read_text())
    for doc in content['documents']:
        path = ROOT/'assets/documents'/doc['filename']
        assert path.read_bytes().startswith(b'%PDF-'), path
    assert not subprocess.check_output(['git', 'ls-files', '.codex-handover/'], cwd=ROOT)
    for path in ['.codex-handover/PORTFOLIO_REFINEMENT_CODEX_HANDOVER_2026-10-30.md', '.codex-handover/PORTFOLIO_CODEX_HANDOVER_READY_TO_COPY_2026-10-30.zip']:
        subprocess.run(['git', 'check-ignore', '-q', path], cwd=ROOT, check=True)
    assert not errors, '\n'.join(errors)
    print(f'PASS: {len(pages)} HTML pages parsed, {checked} relative references checked; CV order, homepage sections, overview lengths, PDFs, UAS hash and ignored handovers verified.')


if __name__ == '__main__':
    check()
