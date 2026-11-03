import {initMotion} from './motion.js';

export function initMenu(root=document){
 const details=root.querySelector('#mobile-menu'),button=details?.querySelector('summary');if(!(details instanceof HTMLDetailsElement)||!button)return;
 const sync=()=>button.setAttribute('aria-expanded',String(details.open));
 const close=()=>{details.open=false;sync()};
 sync();details.addEventListener('toggle',sync);
 details.querySelector('nav')?.addEventListener('click',event=>{if(event.target instanceof Element&&event.target.closest('a'))close()});
 document.addEventListener('keydown',event=>{if(event.key==='Escape'&&details.open){event.preventDefault();close();button.focus()}});
 matchMedia('(min-width:1100px)').addEventListener('change',event=>{if(event.matches)close()});
}
export function initMedia(root=document){root.querySelectorAll('[data-media] img').forEach(img=>{if(!(img instanceof HTMLImageElement))return;const fallback=()=>{img.closest('picture')?.setAttribute('hidden','');img.closest('[data-media]')?.querySelector('.media-placeholder')?.removeAttribute('hidden')};img.addEventListener('error',fallback);if(img.complete&&img.naturalWidth===0)fallback()})}
initMenu();if(!document.body.classList.contains('career-page'))initMotion();initMedia();document.querySelector('[data-print]')?.addEventListener('click',()=>window.print());
