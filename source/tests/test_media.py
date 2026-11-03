import unittest,tempfile,json
from pathlib import Path
from PIL import Image
from tools.media import validate_media,process_image,decode_raster

class MediaTests(unittest.TestCase):
 def test_null_and_path_validation(self):
  data=json.loads(Path('content/project-media.json').read_text());validate_media(data,Path('.'))
  data['projects']['invoiceai']['cover']={'src':'/../../etc/passwd','alt':'Bad','fit':'contain','position':'50% 50%'}
  with self.assertRaises(ValueError):validate_media(data,Path('.'))
 def test_variants_are_bounded_and_hashed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);src=p/'input.png';Image.new('RGB',(1280,800),'white').save(src)
   result=process_image(src,p/'out')
   self.assertEqual(result['width'],1280)
   self.assertEqual([x['width'] for x in result['variants']],[480,800,1280])
   old=result['src'];Image.new('RGB',(1280,800),'black').save(src)
   self.assertNotEqual(old,process_image(src,p/'out')['src'])
 def test_reject_svg_and_animation(self):
  with self.assertRaises(ValueError):decode_raster(b'<svg></svg>','a.svg')
  with self.assertRaises(ValueError):decode_raster(Path('invoice.jpg').read_bytes(),'bad.png')
 def test_portrait_not_upscaled(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);src=p/'x.png';Image.new('RGB',(320,600),'white').save(src)
   result=process_image(src,p/'out');self.assertEqual([v['width'] for v in result['variants']],[320]);self.assertEqual(result['height'],600)

 def test_source_cannot_escape_through_symlink(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);outside=p/'outside';outside.mkdir();Image.new('RGB',(10,10)).save(outside/'x.png');root=p/'root';folder=root/'assets/projects';folder.mkdir(parents=True);(folder/'invoiceai').symlink_to(outside,target_is_directory=True)
   from tools.media import source_path
   with self.assertRaises(ValueError):source_path(root,'invoiceai','/assets/projects/invoiceai/x.png')

 def test_actual_animated_raster_rejected(self):
  from io import BytesIO
  buffer=BytesIO();Image.new('RGB',(20,20),'black').save(buffer,'WEBP',save_all=True,append_images=[Image.new('RGB',(20,20),'white')],duration=100,loop=0)
  with self.assertRaises(ValueError):decode_raster(buffer.getvalue(),'animated.webp')
 def test_cover_schema_rejects_empty_or_wrong_type(self):
  data=json.loads(Path('content/project-media.json').read_text())
  for value in [{},[],False,'']:
   data['projects']['invoiceai']['cover']=value
   with self.assertRaises(ValueError,msg=repr(value)):validate_media(data,Path('.'))
 def test_size_and_pixel_limits(self):
  from io import BytesIO
  from tools.media import MAX_IMAGE
  with self.assertRaises(ValueError):decode_raster(b'0'*(MAX_IMAGE+1),'large.png')
  buffer=BytesIO();Image.new('RGB',(5000,4001)).save(buffer,'PNG')
  with self.assertRaises(ValueError):decode_raster(buffer.getvalue(),'large.png')
