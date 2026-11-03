"""Capture review screenshots against an isolated loopback-only artifact server."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'dist')))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    output=ROOT/'docs/redesign/screenshots';output.mkdir(exist_ok=True)
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
            for width,height in [(1440,1000),(768,1024),(375,812)]:
                page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
                page.goto(f'http://127.0.0.1:{server.server_port}/');page.evaluate('document.fonts.ready')
                page.screenshot(path=str(output/f'home-{width}.png'),full_page=True)
                page.screenshot(path=str(output/f'hero-{width}.png'))
                page.locator('#work').screenshot(path=str(output/f'work-section-{width}.png'))
                if width in [1440,375]:
                    for route,name in [('/pricing/','pricing'),('/services/','services'),('/work/invoiceai/','invoiceai'),('/contact/','contact')]:
                        page.goto(f'http://127.0.0.1:{server.server_port}'+route);page.evaluate('document.fonts.ready');page.screenshot(path=str(output/f'{name}-{width}.png'),full_page=True)
                page.close()
            browser.close()
    finally:server.shutdown();server.server_close();thread.join()
    print('Captured desktop/tablet/375px Home, project panels, and key-page review images.')

if __name__=='__main__':main()
