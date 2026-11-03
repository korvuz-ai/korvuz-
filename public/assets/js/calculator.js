import {calculateEstimate, switchBase} from './pricing-core.js';
import pricing from './pricing-data.js';

/** @param {Element | null} root @param {typeof pricing} pricing */
export function initCalculator(root, pricing) {
 if (!(root instanceof HTMLFormElement)) return;
 const total = root.querySelector('#calcTotal');
 const monthly = root.querySelector('#calcMonthly');
 const estimate = root.querySelector('[data-live-estimate]');
 if (!(total instanceof HTMLElement) || !(monthly instanceof HTMLElement) || !(estimate instanceof HTMLElement)) return;
 root.querySelectorAll('fieldset').forEach(field => {field.disabled = false});
 /** @param {number} value */
 const baht = value => '฿' + value.toLocaleString('en-US');
 const options = [...root.querySelectorAll('input')].filter(input => input.name === 'option');
 const update = () => {
  const selectedBase = root.querySelector('[name=base]:checked');
  if (!(selectedBase instanceof HTMLInputElement)) return;
  const base = pricing.bases.find(item => item.id === selectedBase.value);
  if (!base) return;
  const selected = options.filter(input => input.checked).map(input => input.value);
  const kept = switchBase(base.id, selected, pricing);
  for (const field of root.querySelectorAll('fieldset')) {
   if (!field.dataset.group) continue;
   field.hidden = field.dataset.group !== base.group;
   field.disabled = field.hidden;
  }
  options.forEach(input => {input.checked = kept.includes(input.value)});
  const result = calculateEstimate(base.id, kept, pricing);
  total.textContent = baht(result.once);
  monthly.hidden = result.monthly === 0;
  monthly.textContent = result.monthly ? '+ ' + baht(result.monthly) + ' / เดือน (ดูแลต่อเนื่อง)' : '';
  estimate.hidden = false;
 };
 root.addEventListener('change', update);
 root.addEventListener('submit', event => event.preventDefault());
 update();
}
initCalculator(document.querySelector('[data-calculator]'), pricing);
