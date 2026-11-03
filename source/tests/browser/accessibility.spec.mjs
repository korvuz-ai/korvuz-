import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';

const routes=Object.keys(JSON.parse(fs.readFileSync('dist/release-manifest.json','utf8'))).filter(path=>path.endsWith('index.html')&&path!=='consult/index.html').map(path=>path==='index.html'?'/':'/'+path.replace(/index.html$/,''));
// One route per case gives each scan a clear result and avoids a shared timeout
// hiding unvisited routes when the development host is under unrelated load.
for (const route of routes) {
  test(`WCAG A/AA landmarks and interaction: ${route}`,async({page})=>{
    test.setTimeout(90000);
    await page.goto(route);
    const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
    expect(result.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})),route).toEqual([]);
  });
}
