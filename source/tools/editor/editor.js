let manifest,digest,token,titles,uploads=[],dirty=false,busy=false;const previews=new Map();
const root=document.querySelector('#projects'),status=document.querySelector('#status');
function el(tag,text,attrs={}){const node=document.createElement(tag);if(text!==null)node.textContent=text;Object.entries(attrs).forEach(([k,v])=>node.setAttribute(k,v));return node}
function setBusy(value){busy=value;document.querySelectorAll('button,input,select,textarea').forEach(control=>control.disabled=value)}
function message(text,error=false){status.textContent=text;status.classList.toggle('error',error)}
function changed(){dirty=true;message('Unsaved changes — click Save changes locally when ready.')}
function field(parent,text,value,onchange,type='text'){
 const id=crypto.randomUUID(),label=el('label',text,{for:id}),input=el(type==='textarea'?'textarea':'input',null,{id});if(type!=='textarea')input.type=type;input.value=value;input.addEventListener('input',()=>{onchange(input.value);changed()});parent.append(label,input);return input;
}
function displaySrc(src){return previews.get(src)||src}
async function readFile(file,pid){
 if(file.size>10*1024*1024)throw Error('Each image must be at most 10 MiB.');
 if(!['image/jpeg','image/png','image/webp'].includes(file.type))throw Error('Choose PNG, JPEG, or WebP images.');
 const id=crypto.randomUUID(),data=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result.split(',')[1]);r.onerror=reject;r.readAsDataURL(file)});
 uploads.push({id,projectId:pid,filename:file.name,data});const src='upload:'+id;previews.set(src,URL.createObjectURL(file));return {src,alt:'',fit:'contain',position:'50% 50%'};
}
function picker(parent,labelText,multiple,handler){const id=crypto.randomUUID();parent.append(el('label',labelText,{for:id}));const input=el('input',null,{id,type:'file',accept:'image/png,image/jpeg,image/webp'});input.multiple=multiple;input.addEventListener('change',async()=>{if(busy)return;setBusy(true);try{await handler([...input.files]);changed();render()}catch(e){message(e.message,true)}finally{setBusy(false)}});parent.append(input)}
function slot(pid,item,index){
 const box=el('div',null,{class:'slot'}),visual=el('div'),fields=el('div');
 visual.append(el('p',index<0?'MAIN COVER':`SCREENSHOT ${index+1}`,{class:'label'}));
 if(item){const img=el('img',null,{class:'preview',src:displaySrc(item.src),alt:item.alt||'Selected image preview'});img.style.objectFit=item.fit||'contain';img.style.objectPosition=item.position||'50% 50%';visual.append(img)}else visual.append(el('div','No cover — site will use a clean placeholder',{class:'empty'}));
 picker(visual,index<0?'Choose / replace cover':'Replace screenshot',false,async files=>{if(!files.length)return;const next=await readFile(files[0],pid);if(index<0)manifest.projects[pid].cover=next;else manifest.projects[pid].screenshots[index]={...next,id:item.id,caption:item.caption||''}});
 if(item){
 field(fields,'Alt text (required)',item.alt||'',v=>item.alt=v);
 if(index>=0)field(fields,'Caption (optional)',item.caption||'',v=>item.caption=v,'textarea');
 const id=crypto.randomUUID();fields.append(el('label','Image fit',{for:id}));const select=el('select',null,{id});for(const value of ['contain','cover']){const o=el('option',value==='contain'?'Contain — show complete screenshot':'Cover — crop to fill',{value});o.selected=(item.fit||'contain')===value;select.append(o)}select.addEventListener('change',()=>{item.fit=select.value;changed();render()});fields.append(select);
 const pos=(item.position||'50% 50%').split(' ').map(parseFloat);
 for(const [axis,label] of [[0,'Horizontal focal point'],[1,'Vertical focal point']]){const input=field(fields,label,String(pos[axis]),v=>{pos[axis]=Number(v);item.position=`${pos[0]}% ${pos[1]}%`},'range');input.min='0';input.max='100';input.addEventListener('change',render)}
 const buttons=el('div',null,{class:'slot-actions'});
 for(const [label,act] of [['Remove',()=>{if(index<0)manifest.projects[pid].cover=null;else manifest.projects[pid].screenshots.splice(index,1)}],...(index>=0?[['Move up',()=>{if(index>0){const a=manifest.projects[pid].screenshots;[a[index-1],a[index]]=[a[index],a[index-1]]}}],['Move down',()=>{const a=manifest.projects[pid].screenshots;if(index<a.length-1)[a[index+1],a[index]]=[a[index],a[index+1]]}]]:[])]){const button=el('button',label,{class:'secondary',type:'button'});button.addEventListener('click',()=>{act();changed();render()});buttons.append(button)}fields.append(buttons);
 }else fields.append(el('p','The same cover appears on Home, Work, and the case study. Add a real capture whenever it is ready.'));
 box.append(visual,fields);return box;
}
function render(){root.replaceChildren();for(const [pid,record] of Object.entries(manifest.projects)){const card=el('section',null,{class:'project','data-project':pid});card.append(el('h2',titles[pid]),slot(pid,record.cover,-1));record.screenshots.forEach((x,i)=>card.append(slot(pid,x,i)));picker(card,'Add case-study screenshots (up to 12)',true,async files=>{if(record.screenshots.length+files.length>12)throw Error('Maximum 12 additional screenshots.');const added=[];for(const f of files)added.push({...await readFile(f,pid),id:crypto.randomUUID(),caption:''});record.screenshots.push(...added)});root.append(card)}setBusy(busy)}
async function load(){setBusy(true);try{const res=await fetch('/api/media');if(!res.ok)throw Error('Could not load local media.');const data=await res.json();manifest=data.manifest;digest=data.digest;token=data.token;titles=data.titles;uploads=[];for(const url of previews.values())URL.revokeObjectURL(url);previews.clear();dirty=false;render();message('Loaded. Changes are local until you build and deploy.')}finally{setBusy(false)}}
document.querySelector('#save').addEventListener('click',async e=>{if(busy)return;setBusy(true);message('Saving changes locally…');try{const refs=JSON.stringify(manifest);const used=uploads.filter(u=>refs.includes('upload:'+u.id));for(const record of Object.values(manifest.projects))for(const x of [record.cover,...record.screenshots].filter(Boolean))if(!x.alt.trim())throw Error('Add alt text to every image before saving.');const res=await fetch('/api/media',{method:'POST',headers:{'Content-Type':'application/json','X-Korvuz-Token':token},body:JSON.stringify({version:1,expectedDigest:digest,manifest,uploads:used})});const result=await res.json();if(!res.ok)throw Error(result.error);manifest=result.manifest;digest=result.digest;uploads=[];dirty=false;render();message('Saved locally. Run the build and deploy to update the live site.')}catch(error){message(error.message,true)}finally{setBusy(false)}});
document.querySelector('#discard').addEventListener('click',()=>{if(busy)return;if(!dirty||confirm('Discard unsaved image changes?'))load().catch(e=>message(e.message,true))});
window.addEventListener('beforeunload',e=>{if(dirty||busy){e.preventDefault();e.returnValue=''}});load().catch(e=>message(e.message,true));
