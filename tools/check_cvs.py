#!/usr/bin/env python3
"""Verify generated CV text, layout metadata and clickable URLs against source JSON.

Requires Poppler's pdfinfo/pdftotext; no Python package dependencies.
Render every page for visual review in addition to this check.
"""
import json
import re
import subprocess
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def normalise(text):
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)', '-', text)
    # Poppler may remove a line-end lexical hyphen (e.g. decision-makers).
    text = re.sub(r'(?<=[A-Za-z])-(?=[A-Za-z])', '', text)
    return ' '.join(text.split())


def source_strings(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key not in {'filename', 'link'}:
                yield from source_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from source_strings(item)
    elif isinstance(value, str):
        yield value


def evidence_links(value):
    if isinstance(value, dict):
        if 'link' in value:
            yield value['link']
        for item in value.values():
            yield from evidence_links(item)
    elif isinstance(value, list):
        for item in value:
            yield from evidence_links(item)


def check():
    content = json.loads((ROOT/'tools/cv-content.json').read_text())
    for doc in content['documents']:
        path = ROOT/'assets/documents'/doc['filename']
        info = subprocess.check_output(['pdfinfo', str(path)], text=True)
        pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
        assert pages == len(doc['pages']) == 2, f'{path.name}: unexpected page spill ({pages})'
        assert re.search(r'^Tagged:\s+yes', info, re.M), 'Expected tagged PDF'
        assert '(A4)' in info, 'Expected A4 page size'
        raw_text = subprocess.check_output(['pdftotext', str(path), '-'], text=True)
        text = normalise(raw_text)
        for expected in source_strings(doc):
            assert normalise(expected) in text, f'{path.name}: text missing or truncated: {expected}'
        emails = set(re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]+', text))
        assert emails == {content['email']}, f'{path.name}: unexpected public email'
        assert not re.search(r'£|\b(?:100k|1m|100,000|1,000,000|50 suppliers|30\+ contracts|Best Griller)\b', text, re.I), 'Unapproved private claim'
        url_info = subprocess.check_output(['pdfinfo', '-url', str(path)], text=True)
        urls = {line.split()[-1] for line in url_info.splitlines()[1:] if line.split()}
        expected_urls = {content['portfolio'], content['github'], content['linkedin'], 'mailto:'+content['email'], *evidence_links(doc)}
        assert expected_urls <= urls, f'{path.name}: missing clickable links: {expected_urls-urls}'
        for url in urls:
            parts = urlsplit(url)
            if parts.netloc == 'nusnaaa.github.io':
                target = ROOT / (parts.path.lstrip('/') or 'index.html')
                assert target.is_file(), f'{path.name}: broken portfolio target: {url}'
        print(f'PASS: {path.name} — {pages} tagged A4 pages, all source text present, {len(urls)} clickable URLs checked')


if __name__ == '__main__':
    check()
