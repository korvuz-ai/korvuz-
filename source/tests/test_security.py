import unittest,tempfile,json,base64,threading,http.client,shutil
from pathlib import Path
from unittest.mock import patch
from tools.media_editor import create_server,save_media,manifest_digest,MAX_BODY
from tools.content import PROJECT_IDS
class LocalEditorSecurityTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);(self.root/'content').mkdir()
  self.manifest={'version':1,'projects':{p:{'cover':None,'screenshots':[]} for p in PROJECT_IDS}}
  (self.root/'content/project-media.json').write_text(json.dumps(self.manifest));shutil.copy('content/projects.json',self.root/'content/projects.json')
  self.server=create_server(self.root,0);self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start();self.port=self.server.server_port
 def tearDown(self):self.server.shutdown();self.server.server_close();self.thread.join();self.temp.cleanup()
 def call(self,method,path='/',body=None,headers=None):
  conn=http.client.HTTPConnection('127.0.0.1',self.port,timeout=10);conn.request(method,path,body,headers or {});res=conn.getresponse();code=res.status;data=res.read();conn.close();return code,data
 def session(self):return json.loads(self.call('GET','/api/media')[1])
 def test_origin_host_and_token_protection(self):
  sess=self.session();body=json.dumps({'version':1,'manifest':self.manifest,'uploads':[],'expectedDigest':sess['digest']})
  headers={'Content-Type':'application/json','Origin':f'http://127.0.0.1:{self.port}','X-Korvuz-Token':sess['token']}
  for key,bad in [('Origin','https://evil.test'),('Host','evil.test'),('X-Korvuz-Token','bad')]:
   self.assertEqual(self.call('POST','/api/media',body,{**headers,key:bad})[0],403)
  self.assertEqual(self.call('GET','/api/media',headers={'Host':'evil.test'})[0],403)
  self.assertEqual(self.call('POST','/api/media',body,headers)[0],200)
 def test_request_size_and_path_limits(self):
  sess=self.session();headers={'Content-Type':'application/json','Origin':f'http://127.0.0.1:{self.port}','X-Korvuz-Token':sess['token'],'Content-Length':str(MAX_BODY+1)}
  self.assertEqual(self.call('POST','/api/media',b'',headers)[0],413)
  self.assertEqual(self.call('GET','/assets/projects/invoiceai/../../../../etc/passwd')[0],404)
 def test_failed_replace_preserves_active_manifest(self):
  digest=manifest_digest(self.root)
  with patch('tools.media_editor.os.replace',side_effect=OSError('disk error')):
   with self.assertRaises(OSError):save_media(self.root,{'version':1,'manifest':self.manifest,'uploads':[]},digest)
  self.assertEqual(manifest_digest(self.root),digest)
