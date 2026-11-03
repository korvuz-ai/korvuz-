import {test,expect} from '@playwright/test';
test('career Home prioritizes the resume and keeps Local a small external gateway',async({page})=>{
 await page.goto('/');await expect(page.locator('h1')).toHaveText('Nuntawat Fangritlong');
 await expect(page.locator('main .project-card,main .price-card')).toHaveCount(0);
 await expect(page.locator('main a[href="https://local.korvuz.site/"]')).toHaveCount(1);
 await expect(page.locator('main a[href="/resume/"]')).toBeVisible();
 await expect(page.locator('main a[href="/experience/"]')).toBeVisible();
 await expect(page.locator('.career-highlights')).not.toContainText('%');
});
