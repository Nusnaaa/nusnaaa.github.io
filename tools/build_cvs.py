#!/usr/bin/env python3
"""Build the two CVs from reviewed content; requires Python Playwright + Chromium.

Run: python tools/build_cvs.py
Only PDF generation uses Playwright; the website has no build/runtime dependency.
Review rendered pages and extracted text after changing tools/cv-content.json.
"""
import json
from html import escape
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
STYLE = '''
@page { size: A4; margin: 13mm 16mm 16mm; }
* { box-sizing: border-box; }
body { font: 10pt/1.38 Arial, sans-serif; color: #171717; margin: 0; }
h1 { font-size: 24pt; margin: 0 0 3mm; letter-spacing: -.6pt; }
.role { color: #173f5f; font-size: 12pt; margin: 0 0 3mm; }
.contact { font-size: 9pt; margin-bottom: 5mm; }
a { color: #173f5f; text-decoration: none; }
h2 { font-size: 11.5pt; margin: 4mm 0 2mm; padding-bottom: 1mm; border-bottom: .6pt solid #b8c6cf; color: #173f5f; break-after: avoid; }
h3 { font-size: 10.5pt; margin: 3mm 0 1mm; break-after: avoid; }
p { margin: 1.5mm 0 2mm; } ul { margin: 1.5mm 0 2.5mm; padding-left: 4.5mm; }
li { margin-bottom: 1.4mm; } .subtitle { color: #4c4c4c; font-size: 9pt; break-after: avoid; }
.evidence { font-size: 9pt; margin-bottom: 3mm; }
.page + .page { break-before: page; }
.continuation { font-size: 11pt; font-weight: bold; margin: 0 0 4mm; color: #173f5f; }
li, p { orphans: 2; widows: 2; }
body.compact { font-size: 10pt; line-height: 1.25; }
.compact h2 { margin-top: 3mm; }
.compact h3 { margin-top: 2mm; }
.compact li { margin-bottom: 1mm; }
.compact p { margin-top: 1mm; margin-bottom: 1.5mm; }
.compact ul { margin-top: 1mm; margin-bottom: 2mm; }
'''


def body_content(block):
    result = ''.join(f'<p>{escape(p)}</p>' for p in block.get('paragraphs', []))
    if block.get('bullets'):
        result += '<ul>' + ''.join(f'<li>{escape(p)}</li>' for p in block['bullets']) + '</ul>'
    for entry in block.get('entries', []):
        result += f'<h3>{escape(entry["title"])}</h3><p class="subtitle">{escape(entry["subtitle"])}</p>'
        result += body_content(entry)
        if entry.get('link'):
            result += f'<p class="evidence"><a href="{escape(entry["link"])}">Project overview and technical evidence →</a></p>'
    return result


def build():
    data = json.loads((ROOT / 'tools/cv-content.json').read_text())
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--no-sandbox'])
        for doc in data['documents']:
            compact = 'compact' if len(doc['pages']) == 1 else ''
            html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{escape(data["name"])} — {escape(doc["title"])}</title><style>{STYLE}</style></head><body class="{compact}">'
            for index, blocks in enumerate(doc['pages']):
                html += '<main class="page">' if index == 0 else '<section class="page">'
                if index == 0:
                    html += f'<h1>{escape(data["name"])}</h1><p class="role">{escape(doc["title"])}</p>'
                    html += f'<p class="contact"><a href="mailto:{data["email"]}">{data["email"]}</a><br>'
                    html += f'<a href="{data["portfolio"]}">nusnaaa.github.io</a> · <a href="{data["github"]}">GitHub: Nusnaaa</a> · <a href="{data["linkedin"]}">LinkedIn: linus-adzanku</a></p>'
                else:
                    html += f'<p class="continuation">{escape(data["name"])} · {escape(doc["title"])}</p>'
                for block in blocks:
                    html += f'<h2>{escape(block["heading"])}</h2>' + body_content(block)
                html += '</main>' if index == 0 else '</section>'
            html += '</body></html>'
            page = browser.new_page()
            page.set_content(html)
            path = ROOT / 'assets/documents' / doc['filename']
            page.pdf(path=str(path), prefer_css_page_size=True, print_background=True, tagged=True,
                     display_header_footer=True, header_template='<span></span>',
                     footer_template='<div style="width:100%;text-align:center;font:8px Arial;color:#626262">Linus Adzanku · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
            page.close()
            print(path.relative_to(ROOT))
        browser.close()


if __name__ == '__main__':
    build()
