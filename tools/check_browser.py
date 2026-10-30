#!/usr/bin/env python3
"""Run with Python Playwright against a local static server; saves screenshots outside the repo."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,argparse
ap=argparse.ArgumentParser();ap.add_argument("origin",nargs="?",default="http://127.0.0.1:8000");ap.add_argument("--output",default="/tmp/portfolio-browser-check");args=ap.parse_args()
out=Path(args.output);out.mkdir(exist_ok=True)
pages=['index.html','projects.html','cv.html','projects/aeroacoustics-overview.html','projects/rocket-engine-overview.html','projects/aeroacoustics.html','projects/rocket-engine.html','projects/uas.html'];rows=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(args=['--no-sandbox'])
 for w in [320,375,390,768,1440]:
  page=b.new_page(viewport={'width':w,'height':900},reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
  for name in pages:
   page.goto(args.origin.rstrip('/')+'/'+name,wait_until='domcontentloaded');page.wait_for_timeout(300)
   overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth')
   if overflow:
    print('OVERFLOW',w,name,page.evaluate('''() => [...document.querySelectorAll('main *')].filter(e=>e.getBoundingClientRect().right>innerWidth).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,60)}))'''),flush=True)
   assert not overflow,(w,name)
   links=page.locator('.nav-links a');assert links.all_text_contents()==['Home','Projects','CV','GitHub','Contact']
   assert all(links.nth(i).is_visible() for i in range(5))
   page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement')
   assert page.locator('.skip-link').bounding_box()['y']>=0
   assert page.locator('.skip-link').evaluate('(e)=>getComputedStyle(e).outlineStyle')=='solid'
   page.keyboard.press('Enter');assert page.evaluate('document.activeElement.id')=='main-content'
   assert not page.evaluate('''() => [...document.querySelectorAll('a[href^="#"]')].filter(e=>!document.getElementById(decodeURIComponent(e.hash.slice(1)))).map(e=>e.href)''')
   if 'overview' in name:assert page.locator('.project-toc').count()==0
   if name in ['projects/aeroacoustics.html','projects/rocket-engine.html','projects/uas.html']:
    page.wait_for_selector('.project-toc__toggle');toggle=page.locator('.project-toc__toggle')
    if toggle.is_visible():
     toggle.focus();page.keyboard.press('Enter');assert toggle.get_attribute('aria-expanded')=='true';page.keyboard.press('Escape');assert toggle.get_attribute('aria-expanded')=='false'
     toggle.focus();page.keyboard.press('Enter');page.wait_for_function('document.activeElement.id==="project-toc-panel"')
    link=page.locator('.project-toc__link').nth(1);link.focus();page.keyboard.press('Enter');assert page.evaluate('location.hash')==link.get_attribute('href')
    assert page.evaluate('document.activeElement.id')==link.get_attribute('href')[1:]
   if name=='projects/rocket-engine.html':
    slider=page.locator('#rocket-port-input');before=page.locator('#rocket-final-port').inner_text();assert before!='—';slider.focus();page.keyboard.press('ArrowRight');assert page.locator('#rocket-final-port').inner_text()!=before
    page.locator('#rocket-model-reset').focus();page.keyboard.press('Enter');assert page.locator('#rocket-final-port').inner_text()==before
   page.goto(args.origin.rstrip('/')+'/'+name,wait_until='domcontentloaded');page.wait_for_timeout(150)
   page.screenshot(path=str(out/(name.replace('/','-')+f'-{w}.png')))
   page.locator('.nav-links a').last.focus();page.keyboard.press('Enter');page.wait_for_url('**/index.html#contact');assert page.locator('#contact').is_visible()
   rows.append({'page':name,'width':w,'status':'pass'});print(w,name,'PASS',flush=True)
  page.close()
 b.close()
assert not errors,errors
(out/'results.json').write_text(json.dumps(rows,indent=2));print('PASS: 40 viewport/page combinations, runtime anchors, skip links, shared nav, TOCs and rocket model; no JS errors',flush=True)
