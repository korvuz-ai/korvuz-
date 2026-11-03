import {test, expect} from '@playwright/test';
import fs from 'node:fs';

const routes=Object.keys(JSON.parse(fs.readFileSync('content/seo.json','utf8'))).filter(route=>route!=='/consult/');

test('production pages have complete metadata and no failed assets or console errors', async ({page}) => {
  test.setTimeout(180000);
  const failures=[];
  page.on('console', message => {if(message.type()==='error') failures.push(message.text())});
  page.on('pageerror', error => failures.push(error.message));
  page.on('response', response => {if(response.status()>=400)failures.push(response.status()+' '+response.url())});
  page.on('requestfailed', request => {if(!request.failure()?.errorText.includes('ERR_ABORTED'))failures.push(request.url()+' '+request.failure()?.errorText)});
  for(const route of routes){
    await page.goto(route);
    await page.evaluate(()=>document.fonts.ready);
    await page.locator('footer').scrollIntoViewIfNeeded();
    await page.waitForLoadState('networkidle');
    expect(await page.title(),route).not.toBe('');
    await expect(page.locator('meta[name="description"]')).toHaveCount(1);
    await expect(page.locator('meta[name="description"]')).not.toHaveAttribute('content','');
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href','https://korvuz.site'+route);
    await expect(page.locator('meta[name="viewport"]')).toHaveCount(1);
    await expect(page.locator('link[rel="icon"]')).toHaveCount(1);
    const icon=await page.locator('link[rel="icon"]').getAttribute('href');
    expect((await page.request.get(icon)).status()).toBe(200);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route).toBeTruthy();
  }
  expect(failures).toEqual([]);
});

test('professional contact prepares an encoded email draft',async({page})=>{
 await page.goto('/contact/');await expect(page.locator('[data-professional-contact]')).toBeVisible();
 await page.locator('#contact-name').fill('Recruiter');await page.locator('#contact-email').fill('reply@example.com');await page.locator('#contact-topic').selectOption('Job opportunity');await page.locator('#contact-message').fill('DevOps opportunity');
 const draft=await page.evaluate(async()=>{const {composeProfessionalInquiry}=await import('/assets/js/career-contact.js');return composeProfessionalInquiry(Object.fromEntries(new FormData(document.querySelector('[data-professional-contact]'))),'nuntawat.works@gmail.com')});
 expect(decodeURIComponent(draft)).toContain('Job opportunity');expect(decodeURIComponent(draft)).toContain('DevOps opportunity');expect(draft.startsWith('mailto:nuntawat.works@gmail.com?')).toBeTruthy();
});

test('contain project covers keep their full image frame during hover', async ({page}) => {
  test.skip(page.viewportSize().width < 900);
  await page.goto('/work/');
  const link = page.locator('[data-project="invoiceai"] .project-image-link');
  await link.hover({position:{x:20,y:20}});
  await expect(page.locator('[data-project="invoiceai"] img')).toHaveCSS('transform','none');
  // Moving the media frame keeps the screenshot itself inside its clipping box.
  await expect.poll(() => link.evaluate(el => {
    const frame=el.querySelector('[data-media]').getBoundingClientRect();
    const image=el.querySelector('img').getBoundingClientRect();
    return image.left >= frame.left-.5 && image.right <= frame.right+.5 && image.top >= frame.top-.5 && image.bottom <= frame.bottom+.5;
  })).toBeTruthy();
});
