import {chromium} from '@playwright/test';
import fs from 'node:fs';

const origin=process.env.HUB_PREVIEW_URL||'http://127.0.0.1:8765';
if(!/^http:\/\/127\.0\.0\.1:\d+$/.test(origin))throw new Error('Use a loopback-only local build preview.');
const output='docs/redesign/hub-preview';
fs.mkdirSync(output,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
try{
 for(const width of [1440,768,375]){
  const context=await browser.newContext({viewport:{width,height:width===1440?1000:width===768?1024:812},reducedMotion:'reduce'});
  const page=await context.newPage();
  await page.goto(origin+'/');
  await page.evaluate(()=>document.fonts.ready);
  // Visit every lazy image before capture; jumping straight to the footer can
  // leave valid offscreen images undecoded in a full-page screenshot.
  for(const image of await page.locator('img').all()){
   await image.scrollIntoViewIfNeeded();
   await image.evaluate(async el=>{await el.decode()});
  }
  await page.evaluate(()=>scrollTo(0,0));
  await page.screenshot({path:`${output}/home-${width}.png`,fullPage:true});
  await page.screenshot({path:`${output}/hero-${width}.png`});
  console.log(`Captured ${width}px; no missing images; document width ${await page.evaluate(()=>document.documentElement.scrollWidth)}px`);
  await context.close();
 }
}finally{await browser.close()}
