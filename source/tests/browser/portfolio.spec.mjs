import {test,expect} from '@playwright/test';
import fs from 'node:fs';
const routes=Object.keys(JSON.parse(fs.readFileSync('dist/release-manifest.json','utf8'))).filter(path=>path.endsWith('index.html')&&path!=='consult/index.html').map(path=>path==='index.html'?'/':'/'+path.replace(/index.html$/,''));
test('every page loads with no errors or horizontal overflow',async({page})=>{
 test.setTimeout(180000);const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const route of routes){const res=await page.goto(route);expect(res.status(),route).toBe(200);await expect(page.locator('h1')).toHaveCount(1);await page.evaluate(()=>document.fonts.ready);expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route+' overflow').toBeTruthy();expect(await page.locator('a[href="mailto:nuntawat.works@gmail.com"]').count(),route).toBeGreaterThan(0)}expect(errors).toEqual([]);
});
test('legacy projects retain shared covers, independent links and graceful image fallback',async({page})=>{
 await page.goto('/work/');const cover=page.locator('[data-project="invoiceai"] img');await expect(cover).toHaveCSS('object-fit','contain');const src=await cover.getAttribute('src');
 await page.goto('/work/invoiceai/');expect(await page.locator('.case-cover img').getAttribute('src')).toBe(src);await expect(page.locator('.case-heading')).toContainText('Live demo temporarily unavailable');
 await page.goto('/work/devops-kb/');await expect(page.getByRole('link',{name:'Open Product',exact:false})).toHaveAttribute('href','https://doc.korvuz.site/');
 await page.goto('/work/english-reader/');await expect(page.locator('.case-cover .media-placeholder')).toBeVisible();const before=await page.locator('.case-cover').boundingBox();
 await page.route('**/assets/media/**',route=>route.abort());await page.goto('/work/invoiceai/');await expect(page.locator('.case-cover .media-placeholder')).toBeVisible();const after=await page.locator('.case-cover').boundingBox();expect(Math.abs(after.height-before.height)).toBeLessThan(1);
});
