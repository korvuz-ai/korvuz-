"""Two static text weights keep the first mobile view small and deterministic."""
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

def build_fonts(root:Path,output:Path)->list[Path]:
    output.mkdir(parents=True,exist_ok=True);files=[];notices=[]
    for name in ['Inter','NotoSansThai']:
        source=root/'.tools'/f'{name}.ttf'
        for weight,suffix in [(400,''),(600,'-Semibold')]:
            target=output/f'{name}{suffix}.woff2'
            if target.exists():files.append(target);continue
            font=TTFont(source,recalcTimestamp=False)
            for record in font['name'].names:
                if record.nameID in [0,13,14]:
                    try:text=record.toUnicode()
                    except UnicodeError:continue
                    if text not in notices:notices.append(text)
            if 'fvar' in font:
                axes={axis.axisTag:(weight if axis.axisTag=='wght' else axis.defaultValue) for axis in font['fvar'].axes}
                font=instantiateVariableFont(font,axes,inplace=True)
            options=subset.Options();options.flavor='woff2';options.recalc_timestamp=False;options.layout_features=['*']
            sub=subset.Subsetter(options=options);sub.populate(unicodes=list(range(0x20,0x250))+list(range(0x0e00,0x0e80))+[0x2013,0x2014,0x2018,0x2019,0x201c,0x201d,0x2026,0x2192,0x2197]);sub.subset(font);font.flavor='woff2';font.save(target);files.append(target)
    if notices:(output/'LICENSE.txt').write_text('\n\n'.join(notices)+'\n')
    return files
