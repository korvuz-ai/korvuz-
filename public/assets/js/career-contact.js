/** @param {{name?:string,email?:string,topic?:string,message?:string}} fields @param {string} recipient */
export function composeProfessionalInquiry(fields,recipient){
 if(!/^[A-Za-z0-9._+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/.test(recipient))throw new Error('Invalid recipient');
 const limits={name:100,email:320,topic:100,message:5000};
 for(const [key,limit] of Object.entries(limits))if(String(fields[/** @type {keyof typeof limits} */(key)]||'').length>limit)throw new Error('Message exceeds draft limits');
 const topic=(fields.topic||'Professional connection').replace(/[\r\n]/g,' ').trim();
 const body=[['Name',fields.name],['Reply email',fields.email],['Message',fields.message]].filter(([,value])=>value?.trim()).map(([label,value])=>label+': '+value?.trim()).join('\n\n');
 const url='mailto:'+recipient+'?subject='+encodeURIComponent('KORVUZ / '+topic)+'&body='+encodeURIComponent(body);
 if(url.length>8000)throw new Error('Draft is too long for an email link. Please email directly.');
 return url;
}
if(typeof document!=='undefined'){
 const form=document.querySelector('[data-professional-contact]');
 const status=document.querySelector('#professional-contact-status');
 if(form instanceof HTMLFormElement && status instanceof HTMLElement){
  const recipient=form.dataset.recipient||'';
  try{composeProfessionalInquiry({},recipient);form.hidden=false}catch{status.textContent='Please use the direct email link.'}
  form.addEventListener('submit',event=>{
   event.preventDefault();
   const fields=Object.fromEntries([...new FormData(form)].map(([key,value])=>[key,String(value)]));
   try{
    const url=composeProfessionalInquiry(fields,recipient);
    status.textContent='Opening your email app. Review the draft and send it when ready. If it does not open, use the direct email link.';
    window.location.href=url;
   }catch(error){status.textContent=error instanceof Error?error.message:'Please use the direct email link.'}
  });
 }
}
