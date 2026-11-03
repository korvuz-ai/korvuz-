"""Raster-only media validation and deterministic, bounded responsive derivatives."""
from pathlib import Path
from io import BytesIO
import hashlib,re,warnings
from PIL import Image,ImageOps,UnidentifiedImageError
from tools.content import PROJECT_IDS

MAX_IMAGE=10*1024*1024
MAX_PIXELS=20_000_000
FORMATS={'JPEG':{'.jpg','.jpeg'},'PNG':{'.png'},'WEBP':{'.webp'}}

def decode_raster(data:bytes, filename:str):
    if len(data)>MAX_IMAGE:raise ValueError('Image exceeds 10 MiB')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error',Image.DecompressionBombWarning)
            with Image.open(BytesIO(data)) as image:
                if image.format not in FORMATS or Path(filename).suffix.lower() not in FORMATS[image.format]:raise ValueError('Use a matching PNG, JPEG or WebP filename')
                if getattr(image,'n_frames',1)!=1:raise ValueError('Animated images are not supported')
                if image.width*image.height>MAX_PIXELS:raise ValueError('Image exceeds 20 megapixels')
                image.load(); image=ImageOps.exif_transpose(image)
                mode='RGBA' if 'A' in image.getbands() else 'RGB'
                clean=Image.new(mode,image.size);clean.paste(image.convert(mode));return clean
    except (UnidentifiedImageError,OSError,Image.DecompressionBombError,Image.DecompressionBombWarning) as e:raise ValueError('Invalid raster image') from e

def source_path(root:Path,project_id:str,src:str)->Path:
    prefix=f'/assets/projects/{project_id}/'
    if not isinstance(src,str) or not src.startswith(prefix):raise ValueError('Image must be inside its project asset folder')
    allowed=(root/'assets/projects'/project_id).resolve();path=(root/src.lstrip('/')).resolve()
    if not allowed.is_relative_to(root.resolve()) or not path.is_relative_to(allowed) or not path.is_file():raise ValueError('Missing or unsafe media source: '+src)
    return path

def validate_media(manifest:dict,root:Path)->dict:
    if not isinstance(manifest,dict) or manifest.get('version')!=1 or set(manifest.get('projects',{}))!=set(PROJECT_IDS):raise ValueError('Media manifest requires version 1 and the five project IDs')
    for pid,record in manifest['projects'].items():
        if not isinstance(record,dict) or set(record)!= {'cover','screenshots'}:raise ValueError('Invalid media record')
        cover=record['cover']
        if cover is not None and not isinstance(cover,dict):raise ValueError('Cover must be an image record or null')
        gallery=record['screenshots']
        if not isinstance(gallery,list) or len(gallery)>12:raise ValueError('At most 12 screenshots per project')
        ids=set()
        for item in ([cover] if cover is not None else [])+gallery:
            if not isinstance(item,dict) or not isinstance(item.get('alt'),str) or not item['alt'].strip() or len(item['alt'])>1000:raise ValueError('Every uploaded image needs alt text (max 1000 characters)')
            if item.get('fit','contain') not in ['contain','cover']:raise ValueError('Fit must be contain or cover')
            position=item.get('position','50% 50%')
            if not isinstance(position,str) or not re.fullmatch(r'(?:100|[0-9]{1,2})(?:\.[0-9]+)?% (?:100|[0-9]{1,2})(?:\.[0-9]+)?%',position) or any(float(x.rstrip('%'))>100 for x in position.split()):raise ValueError('Position must be two percentages between 0 and 100')
            if not isinstance(item.get('caption',''),str) or len(item.get('caption',''))>4000:raise ValueError('Invalid caption')
            path=source_path(root,pid,item.get('src'))
            decode_raster(path.read_bytes(),path.name)
        for item in gallery:
            sid=item.get('id')
            if not isinstance(sid,str) or not re.fullmatch('[a-z0-9-]{1,80}',sid) or sid in ids:raise ValueError('Gallery IDs must be unique safe identifiers')
            ids.add(sid)
    return manifest

def process_image(source:Path,output:Path)->dict:
    data=source.read_bytes();image=decode_raster(data,source.name)
    digest=hashlib.sha256(data).hexdigest()[:16];output.mkdir(parents=True,exist_ok=True)
    widths=[w for w in [480,800,1280,1600] if w<=image.width]
    if not widths or image.width<1600 and image.width not in widths:widths.append(image.width)
    variants=[]
    for width in sorted(widths):
        height=round(image.height*width/image.width);size=image.resize((width,height),Image.Resampling.LANCZOS)
        name=f'{digest}-{width}';webp=output/f'{name}.webp';fallback=output/f'{name}.jpg'
        size.save(webp,'WEBP',quality=84,method=6)
        if size.mode=='RGBA':
            bg=Image.new('RGB',size.size,'#111019');bg.paste(size,mask=size.getchannel('A'));size=bg
        size.save(fallback,'JPEG',quality=88,optimize=True)
        variants.append({'width':width,'height':height,'url':'/assets/media/'+fallback.name,'webp':'/assets/media/'+webp.name})
    return {'width':image.width,'height':image.height,'src':variants[-1]['url'],'variants':variants}
