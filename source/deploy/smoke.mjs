import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {chromium, request} from 'playwright';

const origin=new URL(process.argv[2]||'http://127.0.0.1:8765').origin;
assert.ok(['korvuz.site','127.0.0.1','localhost'].includes(new URL(origin).hostname));
const output=path.resolve(process.argv[3]||'test-results/deployment-smoke');
fs.mkdirSync(output,{recursive:true});
const routes=Object.keys(JSON.parse(fs.readFileSync('dist/release-manifest.json','utf8'))).filter(name=>name.endsWith('index.html')&&name!=='consult/index.html').map(name=>name==='index.html'?'/':'/'+name.replace(/index.html$/,''));
const unavailable=new Set(['invoice.korvuz.site','crm.korvuz.site','line.korvuz.site','en.korvuz.site']);
const report={origin,startedAt:new Date().toISOString(),viewports:[],redirects:[],assets:[],passed:false};
const client=await request.newContext({baseURL:origin});
const browser=await chromium.launch({headless:true});
const sha=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
try {
  const manifest=await client.get('/release-manifest.json');
  assert.equal(manifest.status(),200);
  assert.equal(sha(await manifest.body()),sha(fs.readFileSync('dist/release-manifest.json')),'public release must match approved artifact');
  report.version=sha(await manifest.body());
  for(const asset of ['/resume.pdf','/DevOps_Engineer.pdf','/Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf','/assets/icons/mark.svg','/robots.txt','/sitemap.xml']) {
    const response=await client.get(asset);assert.equal(response.status(),200,asset);
    assert.equal(sha(await response.body()),sha(fs.readFileSync('dist'+asset)),asset+' bytes');
    if(asset.endsWith('.pdf'))assert.match(response.headers()['content-type'],/application\/pdf/);
    if(asset.endsWith('.svg'))assert.match(response.headers()['content-type'],/image\/svg\+xml/);
    report.assets.push({path:asset,status:response.status()});
  }
  const sitemap=await (await client.get('/sitemap.xml')).text();
  for(const host of unavailable)assert.ok(!sitemap.includes(host),'sitemap excludes unavailable hosts');
  assert.equal((await client.get('/missing-release-smoke/')).status(),404);
  for(const hidden of ['/content/projects.json','/tools/media_editor.py','/package.json','/docs/redesign/FINAL-QA.md'])assert.equal((await client.get(hidden)).status(),404,hidden+' must not be public');

  for(const width of [1440,375]) {
    const context=await browser.newContext({viewport:{width,height:1000},isMobile:width===375,hasTouch:width===375});
    const page=await context.newPage();const failures=[];
    page.on('pageerror',error=>{if(error.message!=='Transition was skipped')failures.push(error.message)}); // benign Chromium rejection when automation navigates mid view-transition
    page.on('console',message=>{if(message.type()==='error')failures.push({text:message.text(),location:message.location(),page:page.url()})});
    page.on('response',response=>{if(response.status()>=400)failures.push(response.status()+' '+response.url())});
    // Let the site's 120ms native transition finish before automation starts
    // another navigation or changes the reduced-motion preference.
    const visit=async url=>{const response=await page.goto(url);await page.waitForTimeout(160);return response};
    const completed=[];
    for(const route of routes) {
      const response=await visit(origin+route);assert.equal(response.status(),200,route);
      await page.evaluate(()=>document.fonts.ready);
      assert.equal(await page.locator('h1').count(),1,route);
      assert.ok((await page.title()).length>0,route+' title');
      assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'),'https://korvuz.site'+route);
      assert.ok(await page.locator('meta[name="description"]').getAttribute('content'),route+' description');
      assert.equal(await page.locator('link[rel="icon"]').getAttribute('href'),'/assets/icons/mark.svg');
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route+' overflow');
      const destinations=await page.locator('a[href]').evaluateAll(links=>links.map(link=>link.href));
      for(const href of destinations)assert.ok(!unavailable.has(new URL(href).hostname),route+' broken project navigation');
      const imageErrors=await page.locator('img').evaluateAll(async images=>{
        const results=await Promise.all(images.map(async image=>{image.loading='eager';try{await image.decode();return null}catch{return image.src}}));
        return results.filter(Boolean);
      });
      assert.deepEqual(imageErrors,[],route+' images');
      completed.push(route);
    }

    await visit(origin+'/');
    if(width===375) {
      const menu=page.locator('summary.menu-toggle');await menu.focus();await page.keyboard.press('Enter');
      await page.waitForFunction(()=>document.querySelector('#mobile-menu summary')?.getAttribute('aria-expanded')==='true',null,{timeout:2000}).catch(()=>{});
      assert.equal(await menu.getAttribute('aria-expanded'),'true');
      assert.ok(await page.locator('#main-nav a[href="/contact/"]').isVisible());
      await page.keyboard.press('Escape');assert.equal(await menu.getAttribute('aria-expanded'),'false');
      assert.ok(await menu.evaluate(el=>el===document.activeElement));
    }
    assert.equal(await page.locator('h1').innerText(),'Nuntawat Fangritlong');
    assert.equal(await page.locator('.parallax-surface').count(),0);
    assert.equal(await page.locator('main a[href="https://local.korvuz.site/"]').count(),1);
    await page.screenshot({path:path.join(output,'home-'+width+'.png')});
    await visit(origin+'/pricing/');
    assert.equal(await page.locator('#calcTotal').textContent(),'฿8,000');
    for(const option of await page.locator('[data-group="web"] input').all())await option.check();
    assert.equal(await page.locator('#calcTotal').textContent(),'฿22,500');
    assert.match(await page.locator('#calcMonthly').textContent(),/฿2,000/);
    await page.locator('[name=base][value=cloud]').check();assert.equal(await page.locator('#calcTotal').textContent(),'฿15,000');
    assert.ok(await page.locator('#calcMonthly').isHidden());
    for(const option of await page.locator('[data-group="cloud"] input').all())await option.check();
    assert.equal(await page.locator('#calcTotal').textContent(),'฿44,000');
    await page.locator('[name=base][value=static]').check();assert.equal(await page.locator('#calcTotal').textContent(),'฿8,000');
    await visit(origin+'/contact/');
    for(const href of ['mailto:nuntawat.works@gmail.com','https://linkedin.com/in/nuntawat-zeo','https://github.com/korvuz-ai','tel:+66809746514'])assert.ok(await page.locator(`main a[href="${href}"]`).count(),href);
    await page.locator('#contact-name').fill('Deployment smoke test');
    await page.locator('#contact-email').fill('reply@example.com');
    await page.locator('#contact-message').fill('Professional connection & DevOps');
    const draft=await page.evaluate(async()=>{const {composeProfessionalInquiry}=await import('/assets/js/career-contact.js');const form=document.querySelector('[data-professional-contact]');return composeProfessionalInquiry(Object.fromEntries(new FormData(form)),form.dataset.recipient)});
    assert.equal(new URL(draft).pathname,'nuntawat.works@gmail.com');
    assert.ok(new URL(draft).searchParams.get('body').includes('Professional connection & DevOps'));
    await visit(origin+'/lab/');
    const popupPromise=page.waitForEvent('popup');await page.locator('#terminalInput').fill('open invoice');await page.locator('#terminalForm button').click();
    const popup=await popupPromise;await popup.waitForLoadState();assert.equal(popup.url(),origin+'/work/invoiceai/');await popup.close();
    assert.ok((await page.locator('#terminalOutput a').getAttribute('href'))==='/work/invoiceai/');
    await visit(origin+'/work/english-reader/');assert.ok(await page.locator('.case-cover .media-placeholder').isVisible());

    for(const [source,destination] of [['/?ref=smoke#calc','/pricing/?ref=smoke#calculator'],['/index.html?ref=smoke#stack','/about/?ref=smoke#stack'],['/#sandbox','/lab/#terminal'],['/?ref=smoke#work','/work/?ref=smoke'],['/?ref=smoke#experience','/experience/?ref=smoke'],['/consult/?ref=smoke#audit','/services/?ref=smoke#audit'],['/consult?ref=smoke#hourly','/services/?ref=smoke#hourly'],['/consult/index.html?ref=smoke#retainer','/services/?ref=smoke#retainer']]) {
      await visit(origin+source);await page.waitForURL(origin+destination);report.redirects.push({width,source,destination});
    }
    await page.emulateMedia({reducedMotion:'reduce'});await visit(origin+'/');
    assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');
    assert.equal(await page.locator('.parallax-surface').count(),0);
    assert.equal(await page.evaluate(()=>document.getAnimations().filter(animation=>animation.playState==='running').length),0);
    assert.equal(await page.locator('h1').evaluate(el=>getComputedStyle(el).opacity),'1');
    assert.deepEqual(failures,[],'console/network/script errors '+JSON.stringify(failures));
    report.viewports.push({width,routes:completed,calculator:true,contactDraft:true,labFallback:true,englishReaderFallback:true,motion:true,reducedMotion:true,mobileNavigation:width===375});
    await context.close();console.log('PASS',width,'all',completed.length,'routes + interactive journeys');
  }
  if(origin==='https://korvuz.site') {
    for(const source of ['http://korvuz.site/work/?ref=smoke','http://www.korvuz.site/work/?ref=smoke']) {
      const response=await client.get(source,{maxRedirects:0});assert.equal(response.status(),301);
      assert.equal(response.headers().location,source.replace('http:','https:'));report.redirects.push({source,status:301,location:response.headers().location});
    }
    for(const source of ['/consult?ref=smoke','/consult/?ref=smoke','/consult/index.html?ref=smoke']) {
      const response=await client.get(source,{maxRedirects:0});assert.equal(response.status(),301);
      assert.equal(new URL(response.headers().location,origin).href,origin+'/services/?ref=smoke');report.redirects.push({source,status:301,location:response.headers().location});
    }
    const slashless=await client.get('/work?ref=smoke',{maxRedirects:0});assert.equal(slashless.status(),301);assert.equal(new URL(slashless.headers().location,origin).href,origin+'/work/?ref=smoke');
    const html=await client.get('/');assert.match(html.headers()['cache-control'],/no-cache/);
    for(const [name,value] of Object.entries({'x-frame-options':'SAMEORIGIN','x-content-type-options':'nosniff','x-xss-protection':'1; mode=block','referrer-policy':'strict-origin-when-cross-origin'}))assert.equal(html.headers()[name],value,name);
    const media=Object.keys(JSON.parse(fs.readFileSync('dist/release-manifest.json','utf8'))).find(name=>name.startsWith('assets/media/'));
    const mediaResponse=await client.get('/'+media);assert.match(mediaResponse.headers()['cache-control'],/immutable/);
    for(const name of ['x-frame-options','x-content-type-options','x-xss-protection','referrer-policy'])assert.equal(mediaResponse.headers()[name],html.headers()[name],name+' on media');
  }
  for(const route of ['/missing-release-smoke/','/404.html','/404/']){
    const response=await client.get(route);assert.equal(response.status(),404);assert.match(await response.text(),/Page not found\./);assert.match(await response.text(),/noindex/);
    assert.equal((await client.head(route)).status(),404);
  }
  if(origin==='https://korvuz.site'){
    const www=await client.get('https://www.korvuz.site/release-manifest.json');assert.equal(www.status(),200);assert.equal(sha(await www.body()),report.version);
    const local=await client.head('https://local.korvuz.site/');assert.ok([200,401].includes(local.status()),'local gateway reachable (200, or 401 behind staging auth)');report.localGatewayStatus=local.status();
  }
  report.custom404=true;
  report.passed=true;report.finishedAt=new Date().toISOString();console.log('PASS release smoke',report.version);
} catch(error) {
  report.error=error.stack||String(error);console.error(report.error);process.exitCode=1;
} finally {
  fs.writeFileSync(path.join(output,'smoke.json'),JSON.stringify(report,null,2)+'\n');
  await browser.close();await client.dispose();
}
