import {chromium} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';

const width=Number(process.argv[process.argv.indexOf('--width')+1]);
assert.ok([320,375,768,1024,1440].includes(width),'Provide one requested --width.');
const manifest=JSON.parse(fs.readFileSync('dist/release-manifest.json','utf8'));
const routes=Object.keys(manifest).filter(path=>path.endsWith('index.html')&&path!=='consult/index.html').map(path=>path==='index.html'?'/':'/'+path.replace(/index.html$/,''));
const primary=['/','/about/','/resume/','/experience/','/skills/','/contact/'];
const output='docs/redesign/career-preview';fs.mkdirSync(output,{recursive:true});
const server=spawn('python3',['tools/preview.py','--port','0','--directory','dist'],{stdio:['ignore','pipe','pipe']});
const origin=await new Promise((resolve,reject)=>{server.stdout.once('data',data=>resolve(data.toString().trim()));server.once('error',reject);server.once('exit',code=>reject(new Error('Preview exited: '+code)))});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const report={width,routes:[],redirects:[],downloads:[],checks:[],errors:[]};
try{
 const context=await browser.newContext({viewport:{width,height:width<600?900:1000},isMobile:width<600,hasTouch:width<600});
 const page=await context.newPage();
 page.on('pageerror',error=>report.errors.push(error.message));
 page.on('console',message=>{if(message.type()==='error')report.errors.push(message.text())});
 for(const route of routes){
  const response=await page.goto(origin+route);assert.equal(response.status(),200,route);
  await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('h1').count(),1,route);
  assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://korvuz.site'+route);
  assert.ok(await page.locator('meta[name=description]').getAttribute('content'));
  assert.ok(await page.title());
  assert.equal(await page.locator('meta[name=viewport]').count(),1);
  for(const image of await page.locator('img').all()){await image.scrollIntoViewIfNeeded();await image.evaluate(el=>el.decode());assert.ok(await image.evaluate(el=>el.naturalWidth>0&&el.complete))}
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route+' overflow');
  for(const el of await page.locator('script[type="application/ld+json"]').all())JSON.parse(await el.textContent());
  if(primary.includes(route)){
   assert.equal(await page.locator('.parallax-surface').count(),0);
   assert.ok((await page.locator('body').evaluate(el=>getComputedStyle(el).fontFamily)).includes('Inter'));
  }
  const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
  assert.deepEqual(axe.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),[],route+' WCAG');
  if(route==='/'||(primary.includes(route)&&[375,1440].includes(width))){await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${output}/${route==='/'?'home':route.split('/')[1]}-${width}.png`,fullPage:true})}
  report.routes.push({route,status:200,overflow:false,wcagViolations:0});
 }
 assert.deepEqual(report.errors,[],'Canonical route console errors');
 await page.goto(origin+'/');
 assert.equal(await page.locator('h1').innerText(),'Nuntawat Fangritlong');
 assert.equal(await page.locator('main .project-card,main .price-card').count(),0);
 assert.equal(await page.locator('main a[href="https://local.korvuz.site/"]').count(),1);
 assert.ok(await page.locator('main a[href="/resume/"]').isVisible());
 if(width<1100){const summary=page.locator('summary.menu-toggle');await summary.focus();await page.keyboard.press('Enter');assert.equal(await summary.getAttribute('aria-expanded'),'true');assert.ok(await page.locator('#main-nav a[href="/contact/"]').isVisible());await page.keyboard.press('Escape');assert.ok(await summary.evaluate(el=>el===document.activeElement));assert.equal(await summary.getAttribute('aria-expanded'),'false')}
 report.checks.push('career-first Home, small Local teaser, keyboard navigation and focus');
 for(const name of ['resume.pdf','DevOps_Engineer.pdf','Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf']){const response=await context.request.get(origin+'/'+name);assert.equal(response.status(),200);const bytes=await response.body();assert.equal(bytes.subarray(0,4).toString(),'%PDF');assert.ok(response.headers()['content-type'].includes('application/pdf'));assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),manifest[name]);report.downloads.push({name,status:200,originalBytes:true})}
 await page.goto(origin+'/contact/');
 for(const href of ['mailto:nuntawat.works@gmail.com','https://linkedin.com/in/nuntawat-zeo','https://github.com/korvuz-ai','tel:+66809746514','https://local.korvuz.site/'])assert.ok(await page.locator(`main a[href="${href}"]`).count(),href);
 await page.locator('#contact-name').fill('Professional contact');await page.locator('#contact-email').fill('reply@example.com');await page.locator('#contact-message').fill('DevOps & cloud\nสวัสดี');
 const draft=await page.evaluate(async()=>{const{composeProfessionalInquiry}=await import('/assets/js/career-contact.js');const form=document.querySelector('[data-professional-contact]');return composeProfessionalInquiry(Object.fromEntries(new FormData(form)),form.dataset.recipient)});
 assert.equal(new URL(draft).pathname,'nuntawat.works@gmail.com');assert.ok(new URL(draft).searchParams.get('body').includes('DevOps & cloud\nสวัสดี'));
 report.checks.push('canonical contact links and encoded email draft; no message sent');
 const icon=await context.request.get(origin+'/assets/icons/mark.svg');assert.equal(icon.status(),200);assert.ok(icon.headers()['content-type'].includes('image/svg+xml'));
 const sitemap=await context.request.get(origin+'/sitemap.xml');assert.equal(sitemap.status(),200);assert.ok(!(await sitemap.text()).includes('/404'));
 for(const [source,target] of [['/?ref=qa#calc','/pricing/?ref=qa#calculator'],['/index.html?ref=qa#stack','/about/?ref=qa#stack'],['/?ref=qa#work','/work/?ref=qa'],['/?ref=qa#experience','/experience/?ref=qa'],['/?ref=qa#building','/lab/?ref=qa'],['/consult?ref=qa#audit','/services/?ref=qa#audit'],['/consult/index.html?ref=qa#retainer','/services/?ref=qa#retainer']]){await page.goto(origin+source);await page.waitForURL(origin+target);report.redirects.push({source,target})}
 for(const path of ['/consult','/consult/','/consult/index.html']){const response=await context.request.get(origin+path+'?ref=qa',{maxRedirects:0});assert.equal(response.status(),301);assert.equal(response.headers().location,'/services/?ref=qa')}
 for(const path of ['/missing-career-route?ref=qa','/404.html','/404/']){
  const response=await page.goto(origin+path);assert.equal(response.status(),404);assert.equal(await page.locator('h1').innerText(),'Page not found.');assert.ok((await page.locator('meta[name=robots]').getAttribute('content')).includes('noindex'));
  const head=await context.request.head(origin+path);assert.equal(head.status(),404);
  const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();assert.deepEqual(axe.violations.map(v=>v.id),[]);
 }
 if([375,1440].includes(width))await page.screenshot({path:`${output}/404-${width}.png`,fullPage:true});
 report.checks.push('SVG favicon, sitemap, consulting 301s, query/hash redirects and true custom 404/HEAD');
 // Expected custom-404 responses can produce browser resource console messages.
 report.errors=report.errors.filter(error=>!error.includes('404 (Not Found)'));
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto(origin+'/');
 assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');
 assert.equal(await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length),0);
 assert.equal(await page.locator('.parallax-surface').count(),0);report.checks.push('static reduced-motion career pages');
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:900}});const plain=await nojs.newPage();await plain.goto(origin+'/');await plain.locator('summary.menu-toggle').focus();await plain.keyboard.press('Enter');assert.ok(await plain.locator('#main-nav a[href="/resume/"]').isVisible());assert.equal(await plain.locator('summary.menu-toggle').getAttribute('aria-expanded'),null);await plain.goto(origin+'/contact/');assert.ok(await plain.locator('noscript').isVisible());assert.ok(await plain.locator('a[href="mailto:nuntawat.works@gmail.com"]').count());await nojs.close();
 report.checks.push('native keyboard menu and direct contacts without JavaScript');
 assert.deepEqual(report.errors,[]);await context.close();report.passed=true;
 console.log(`PASS ${width}px: ${routes.length} canonical routes, all-route WCAG, downloads, redirects, contacts, navigation, reduced motion and 404.`);
}catch(error){report.passed=false;report.failure=String(error);console.error(error);process.exitCode=1}
finally{fs.writeFileSync(`${output}/qa-${width}.json`,JSON.stringify(report,null,2)+'\n');await browser.close();server.kill()}
