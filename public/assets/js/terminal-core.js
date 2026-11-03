/** @type {Readonly<Record<string, string>>} */
const projects=Object.freeze({devops:'devops-kb',fiatline:'fiatline',invoice:'invoiceai',invoiceai:'invoiceai',linecrm:'linecrm',crm:'linecrm',english:'english-reader'});
const commands=new Set(['help','whoami','ls','status','skills','contact','resume','cv','neofetch','git log','matrix','sudo hire korvuz','clear','exit','sudo exit']);
/** @param {string} alias @param {Readonly<Record<string, string>>} destinations */
export function resolveProject(alias,destinations){return Object.hasOwn(projects,alias)?destinations[projects[alias]]||null:null}
/** @param {string} input */
export function parseCommand(input){const query=input.trim().toLowerCase();if(query.startsWith('open '))return{kind:'open',argument:query.slice(5).trim()};return{kind:commands.has(query)?query:'unknown',argument:input.trim()}}
