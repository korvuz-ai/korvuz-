import test from'node:test';import assert from'node:assert/strict';import{parseCommand,resolveProject}from'../assets/js/terminal-core.js';import{resolveLegacy}from'../assets/js/legacy.js';
const destinations={invoiceai:'/work/invoiceai/',linecrm:'/work/linecrm/',fiatline:'/work/fiatline/','english-reader':'/work/english-reader/','devops-kb':'https://doc.korvuz.site/'};
test('all original commands and aliases',()=>{for(const cmd of ['help','whoami','ls','status','skills','contact','resume','cv','neofetch','git log','matrix','sudo hire korvuz','clear','exit','sudo exit'])assert.notEqual(parseCommand(cmd).kind,'unknown',cmd);assert.equal(resolveProject('crm',destinations),'/work/linecrm/');assert.equal(resolveProject('invoice',destinations),'/work/invoiceai/');assert.equal(resolveProject('https://evil.test',destinations),null);assert.equal(parseCommand('<img onerror=x>').kind,'unknown')});
test('legacy routing preserves queries and known fragments',()=>{assert.equal(resolveLegacy('/','#calc','?ref=old'),'/pricing/?ref=old#calculator');assert.equal(resolveLegacy('/consult/','#audit','?ref=old'),'/services/?ref=old#audit');assert.equal(resolveLegacy('/consult/','',''),'/services/#consulting');assert.equal(resolveLegacy('/','#weird',''),null);assert.equal(resolveLegacy('/','#terminalInput',''),'/lab/#terminal')});
test('every moved legacy fragment preserves the original query on old HTML entrypoints',()=>{
 const moved={'#stack':'/about/#stack','#calc':'/pricing/#calculator','#calcTotal':'/pricing/#calculator','#calcMonthly':'/pricing/#calculator','#sandbox':'/lab/#terminal','#terminalOutput':'/lab/#terminal','#terminalPrompt':'/lab/#terminal','#terminalInput':'/lab/#terminal'};
 for(const path of ['/','/index.html'])for(const [hash,destination] of Object.entries(moved)){
  const [route,fragment]=destination.split('#');
  assert.equal(resolveLegacy(path,hash,'?ref=qa&lang=th'),route+'?ref=qa&lang=th#'+fragment);
 }
 for(const path of ['/consult','/consult/','/consult/index.html'])for(const hash of ['#rates','#hourly','#audit','#retainer']){
  assert.equal(resolveLegacy(path,hash,'?ref=qa'),'/services/?ref=qa'+hash);
 }
});
