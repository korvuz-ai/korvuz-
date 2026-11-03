import {chromium} from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const origin=new URL(process.argv[2]||'https://korvuz.site').origin;
assert.ok(['korvuz.site','127.0.0.1','localhost'].includes(new URL(origin).hostname));
const output=process.argv[3]||'test-results/deploy-live/accessibility.json';
const browser=await chromium.launch({headless:true});
const report={origin,passed:false,checks:[]};
try {
  for(const width of [1440,375]) {
    const context=await browser.newContext({viewport:{width,height:1000}});
    const page=await context.newPage();
    for(const route of ['/','/about/','/resume/','/experience/','/skills/','/contact/','/missing-live-accessibility/']) {
      const response=await page.goto(origin+route);
      assert.equal(response.status(),route.includes('missing-')?404:200);
      const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
      assert.deepEqual(result.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})),[],route);
      report.checks.push({width,route,status:response.status(),violations:0});
    }
    await context.close();
    console.log('PASS live WCAG',width);
  }
  report.passed=true;
} catch(error) {
  report.error=String(error);
  throw error;
} finally {
  fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');
  await browser.close();
}
