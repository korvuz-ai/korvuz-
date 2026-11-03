import {test,expect} from '@playwright/test';
test('career pages stay static and respect reduced motion',async({page})=>{
 for(const route of ['/','/about/','/resume/','/experience/','/skills/','/contact/']){
  await page.goto(route);await expect(page.locator('.parallax-surface')).toHaveCount(0);
 }
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');
 await expect(page.locator('html')).toHaveCSS('scroll-behavior','auto');
 expect(await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').length)).toBe(0);
 await page.locator('main a[href="/resume/"]').focus();await page.keyboard.press('Enter');
 await expect(page).toHaveURL(/\/resume\/$/);await expect(page.locator('h1')).toBeVisible();
});
test('retained project-media parallax stays bounded and preserves image dimensions',async({page})=>{
 test.skip(page.viewportSize().width<900);
 await page.goto('/work/');const link=page.locator('.project-image-link').first();await link.scrollIntoViewIfNeeded();
 const size=await link.locator('img').evaluate(el=>[el.offsetWidth,el.offsetHeight]);
 await link.hover({position:{x:20,y:20}});
 await expect.poll(()=>link.locator('[data-media]').evaluate(el=>new DOMMatrix(getComputedStyle(el).transform).m41)).toBeLessThan(0);
 const offset=await link.locator('[data-media]').evaluate(el=>{const m=new DOMMatrix(getComputedStyle(el).transform);return[m.m41,m.m42]});
 expect(offset.every(n=>Math.abs(n)<=4)).toBeTruthy();
 expect(await link.locator('img').evaluate(el=>[el.offsetWidth,el.offsetHeight])).toEqual(size);
 await page.emulateMedia({reducedMotion:'reduce'});await expect(link.locator('[data-media]')).toHaveCSS('transform','none');
});
