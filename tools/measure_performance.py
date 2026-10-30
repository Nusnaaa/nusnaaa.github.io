#!/usr/bin/env python3
"""Record comparable cold/warm lab performance with Python Playwright and Chromium."""
import argparse,json,datetime,time,importlib.metadata
from pathlib import Path
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('origin');ap.add_argument('output');ap.add_argument('--overview',action='store_true');ap.add_argument('--live',action='store_true');args=ap.parse_args()
pages=['index.html','projects.html','cv.html','projects/aeroacoustics.html','projects/rocket-engine.html']
if args.overview:pages+=['projects/aeroacoustics-overview.html','projects/rocket-engine-overview.html']
rows=[]
with sync_playwright() as p:
 b=p.chromium.launch(args=['--no-sandbox'])
 for name in pages:
  c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
  page=c.new_page();cdp=c.new_cdp_session(page);cdp.send('Network.enable');cdp.send('Network.emulateNetworkConditions',{'offline':False,'latency':80,'downloadThroughput':500000,'uploadThroughput':125000});cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
  page.add_init_script('''window.lab={lcp:null,cls:0};new PerformanceObserver(l=>{for(const e of l.getEntries())window.lab.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.lab.cls+=e.value}).observe({type:'layout-shift',buffered:true});''')
  for cache in ['cold','warm']:
   resources={}
   def response(e):resources.setdefault(e['requestId'],{}).update(url=e['response']['url'],status=e['response']['status'],mime=e['response']['mimeType'],cached=e['response'].get('fromDiskCache',False))
   def chunk(e):
    r=resources.setdefault(e['requestId'],{});r['partialBytes']=r.get('partialBytes',0)+e.get('encodedDataLength',0)
   def finish(e):resources.setdefault(e['requestId'],{}).update(bytes=e['encodedDataLength'])
   cdp.on('Network.responseReceived',response);cdp.on('Network.loadingFinished',finish);cdp.on('Network.dataReceived',chunk)
   if cache=='cold':cdp.send('Network.clearBrowserCache')
   url=args.origin.rstrip('/')+'/'+name
   try:
    page.goto(url,wait_until='domcontentloaded',timeout=60000);page.wait_for_timeout(10000)
    data=page.evaluate('''() => ({ttfb:performance.getEntriesByType('navigation')[0].responseStart,serverWait:performance.getEntriesByType('navigation')[0].responseStart-performance.getEntriesByType('navigation')[0].requestStart,fcp:performance.getEntriesByName('first-contentful-paint')[0]?.startTime,lcp:lab.lcp,cls:lab.cls,domContentLoaded:performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd,resources:performance.getEntriesByType('resource').map(e=>({url:e.name,start:e.startTime,duration:e.duration,transfer:e.transferSize,initiator:e.initiatorType})),navigationVisible:!!document.querySelector('.site-nav')})''')
    vals=list(resources.values());data.update(url=url,cache=cache,time=datetime.datetime.now(datetime.timezone.utc).isoformat(),initialBytes=sum(r.get('bytes',r.get('partialBytes',0)) for r in vals),requests=len(vals),pendingTransfers=sum('bytes' not in r for r in vals),largest=sorted(vals,key=lambda x:x.get('bytes',x.get('partialBytes',0)),reverse=True)[:5]);rows.append(data);print(name,cache,'TTFB',round(data['ttfb']),'FCP',data['fcp'],'LCP',data['lcp'],'CLS',round(data['cls'],4),'bytes',data['initialBytes'],flush=True)
   except Exception as e:rows.append({'url':url,'cache':cache,'error':str(e)});print(str(e),flush=True)
   cdp.remove_listener('Network.responseReceived',response);cdp.remove_listener('Network.loadingFinished',finish);cdp.remove_listener('Network.dataReceived',chunk)
  c.close()
 meta={'tool':'Playwright Python '+importlib.metadata.version('playwright'),'browser':b.version,'viewport':'390x844 CSS px, DPR1, mobile/touch emulation','throttle':'CDP 80ms latency; 4 Mbit/s down, 1 Mbit/s up; CPU slowdown 4x','observation':'10 seconds after DOMContentLoaded, no scrolling or input; completed transfers plus observed partial encoded bytes; captures headers on completed resources; CLS is summed shifts without recent input','cache':'cold=clear browser HTTP cache; warm=repeat in same context (server may revalidate)','kind':'live' if args.live else 'local lab','runs':rows}
 b.close()
 Path(args.output).write_text(json.dumps(meta,indent=2))
