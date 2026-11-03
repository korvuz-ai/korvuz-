"""Loopback-only static production preview with genuine custom 404 responses."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import argparse
from urllib.parse import urlsplit

class PreviewHandler(SimpleHTTPRequestHandler):
    def redirect_consult(self):
        url=urlsplit(self.path)
        if url.path not in ['/consult','/consult/','/consult/index.html']:return False
        self.send_response(301);self.send_header('Location','/services/'+('?' + url.query if url.query else ''));self.send_header('Content-Length','0');self.end_headers();return True

    def do_GET(self):
        if self.redirect_consult():return
        if self.path.split('?',1)[0] in ['/404/','/404.html']:
            self.send_error(404);return
        super().do_GET()

    def do_HEAD(self):
        if self.redirect_consult():return
        if self.path.split('?',1)[0] in ['/404/','/404.html']:self.send_error(404);return
        super().do_HEAD()

    def send_error(self,code,message=None,explain=None):
        page=Path(self.directory)/'404.html'
        if code==404 and page.is_file():
            data=page.read_bytes();self.send_response(404)
            self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)))
            self.send_header('X-Robots-Tag','noindex');self.end_headers()
            if self.command!='HEAD':self.wfile.write(data)
        else:super().send_error(code,message,explain)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);parser.add_argument('--directory',type=Path,default=Path(__file__).resolve().parents[1]/'dist');args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(PreviewHandler,directory=str(args.directory.resolve())))
    print(f'http://127.0.0.1:{server.server_port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
