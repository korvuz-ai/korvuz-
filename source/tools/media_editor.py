"""Local-only, origin-protected project image editor. Not included in dist."""
from __future__ import annotations
from pathlib import Path
import sys
if __package__ in (None,''):sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import argparse,base64,copy,hashlib,json,mimetypes,os,re,secrets,tempfile,threading,webbrowser
from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlsplit,unquote
from tools.content import PROJECT_IDS
from tools.media import validate_media,decode_raster,source_path,MAX_IMAGE

MAX_BODY=70*1024*1024
SAVE_LOCK=threading.Lock()
class EditorError(ValueError):
    def __init__(self,message,status=400,field='media'):super().__init__(message);self.status=status;self.field=field

def manifest_digest(root:Path)->str:return hashlib.sha256((root/'content/project-media.json').read_bytes()).hexdigest()

def save_media(root:Path,payload:dict,expected_digest:str)->dict:
    with SAVE_LOCK:
        if not secrets.compare_digest(manifest_digest(root),str(expected_digest)):raise EditorError('Another save changed the media. Reload before reapplying your changes.',409)
        if not isinstance(payload,dict) or payload.get('version')!=1:raise EditorError('Unsupported request version')
        proposed=copy.deepcopy(payload.get('manifest'));uploads=payload.get('uploads',[])
        if not isinstance(proposed,dict) or not isinstance(uploads,list) or len(uploads)>65:raise EditorError('Invalid upload payload')
        prepared={};total=0
        for upload in uploads:
            if not isinstance(upload,dict):raise EditorError('Invalid upload')
            pid=upload.get('projectId');uid=upload.get('id');filename=upload.get('filename')
            if pid not in PROJECT_IDS or not isinstance(uid,str) or not re.fullmatch('[a-z0-9-]{1,80}',uid) or uid in prepared:raise EditorError('Invalid upload project or ID')
            if not isinstance(filename,str) or len(filename)>255 or not isinstance(upload.get('data'),str):raise EditorError('Invalid filename or data')
            try:data=base64.b64decode(upload['data'],validate=True)
            except (ValueError,TypeError) as e:raise EditorError('Invalid base64 upload') from e
            total+=len(data)
            if len(data)>MAX_IMAGE or total>50*1024*1024:raise EditorError('Upload size limit exceeded',413)
            image=decode_raster(data,filename)
            prepared[uid]={'pid':pid,'image':image,'src':f'/assets/projects/{pid}/{secrets.token_hex(12)}.png'}
        used=set();written=[]
        try:
            records=proposed.get('projects',{})
            if not isinstance(records,dict) or set(records)!=set(PROJECT_IDS):raise EditorError('Five project records are required')
            for pid,record in records.items():
                if not isinstance(record,dict) or not isinstance(record.get('screenshots'),list):raise EditorError('Invalid project record')
                if len(record['screenshots'])>12:raise EditorError('At most 12 screenshots per project')
                for item in ([record.get('cover')] if record.get('cover') else [])+record['screenshots']:
                    if not isinstance(item,dict):raise EditorError('Invalid media item')
                    src=item.get('src','')
                    if isinstance(src,str) and src.startswith('upload:'):
                        uid=src[7:];upload=prepared.get(uid)
                        if not upload or upload['pid']!=pid:raise EditorError('Upload does not match its project')
                        item['src']=upload['src'];used.add(uid)
            if used!=set(prepared):raise EditorError('Unused or missing upload reference')
            # New unique files cannot overwrite the previous manifest's images.
            for uid in used:
                upload=prepared[uid];target=root/upload['src'].lstrip('/')
                allowed=(root/'assets/projects'/upload['pid']).resolve()
                if not allowed.is_relative_to(root.resolve()) or not target.resolve().is_relative_to(allowed):raise EditorError('Unsafe image path')
                target.parent.mkdir(parents=True,exist_ok=True)
                upload['image'].save(target,'PNG');written.append(target)
                # Normalized files must also respect the limit so future builds accept them.
                if target.stat().st_size>MAX_IMAGE:raise EditorError('Normalized image exceeds 10 MiB; use a smaller image',413)
            validate_media(proposed,root)
            path=root/'content/project-media.json'
            fd,tmp=tempfile.mkstemp(prefix='.media-',dir=path.parent)
            try:
                with os.fdopen(fd,'w') as f:json.dump(proposed,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
                os.replace(tmp,path)
            finally:
                if os.path.exists(tmp):os.unlink(tmp)
        except Exception:
            for target in written:target.unlink(missing_ok=True)
            raise
        return {'manifest':proposed,'digest':manifest_digest(root),'saved':True}

def create_server(root:Path,port:int=8766)->HTTPServer:
    root=root.resolve();token=secrets.token_urlsafe(32)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def respond(self,code,data,kind='application/json; charset=utf-8'):
            if kind.startswith('application/json'):data=json.dumps(data,ensure_ascii=False).encode()
            elif isinstance(data,str):data=data.encode()
            self.send_response(code);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','DENY')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' blob: data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers();self.wfile.write(data)
        def host_ok(self):return self.headers.get('Host')==f'127.0.0.1:{self.server.server_port}'
        def do_GET(self):
            if not self.host_ok():return self.respond(403,{'error':'Invalid host'})
            path=urlsplit(self.path).path
            if path=='/api/media':
                manifest=json.loads((root/'content/project-media.json').read_text());titles={p['id']:p['title'] for p in json.loads((root/'content/projects.json').read_text())}
                return self.respond(200,{'manifest':manifest,'digest':manifest_digest(root),'token':token,'titles':titles})
            if path in ['/','/editor.js','/editor.css']:
                file=Path(__file__).parent/'editor'/('index.html' if path=='/' else path[1:])
                return self.respond(200,file.read_bytes(),mimetypes.guess_type(str(file))[0] or 'text/plain')
            if path.startswith('/assets/projects/'):
                parts=unquote(path).split('/')
                try:
                    pid=parts[3]
                    if pid not in PROJECT_IDS:raise ValueError()
                    file=source_path(root,pid,unquote(path))
                    return self.respond(200,file.read_bytes(),mimetypes.guess_type(str(file))[0] or 'application/octet-stream')
                except (ValueError,IndexError):pass
            self.respond(404,{'error':'Not found'})
        def do_POST(self):
            origin=f'http://127.0.0.1:{self.server.server_port}'
            if not self.host_ok() or self.headers.get('Origin')!=origin or not secrets.compare_digest(self.headers.get('X-Korvuz-Token',''),token):return self.respond(403,{'error':'Local session verification failed'})
            if urlsplit(self.path).path!='/api/media':return self.respond(404,{'error':'Not found'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if length<=0:raise EditorError('A JSON body is required')
                if length>MAX_BODY:raise EditorError('Request exceeds 70 MiB',413)
                if self.headers.get('Content-Type','').split(';')[0]!='application/json':raise EditorError('Use application/json')
                payload=json.loads(self.rfile.read(length))
                if not isinstance(payload,dict):raise EditorError('Expected a JSON object')
                result=save_media(root,payload,payload.get('expectedDigest',''));self.respond(200,result)
            except (ValueError,TypeError,KeyError) as e:self.respond(getattr(e,'status',400),{'error':str(e),'field':getattr(e,'field','media')})
            except OSError:self.respond(500,{'error':'Could not save media. The previous manifest is unchanged.','field':'media'})
    server=HTTPServer(('127.0.0.1',port),Handler);server.timeout=10;return server

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8766);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--no-open',action='store_true');args=parser.parse_args()
    server=create_server(args.root,args.port);url=f'http://127.0.0.1:{server.server_port}/';print('Korvuz local media editor:',url,flush=True)
    if not args.no_open:webbrowser.open(url)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
