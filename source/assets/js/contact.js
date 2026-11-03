/** @param {{projectType?: string, description?: string, budget?: string, timeline?: string}} fields */
export function composeInquiry(fields) {
 const body = [['Project type', fields.projectType], ['Details', fields.description], ['Budget', fields.budget], ['Timeline', fields.timeline]]
  .filter(([, value]) => value?.trim()).map(([label, value]) => label + ': ' + value?.trim()).join('\n\n');
 return 'mailto:korvuznox@gmail.com?subject=' + encodeURIComponent('สอบถามโปรเจกต์ / Korvuz') + '&body=' + encodeURIComponent(body);
}
if (typeof document !== 'undefined') {
 const form = document.querySelector('[data-contact]');
 const status = document.querySelector('#contact-status');
 if (form instanceof HTMLFormElement && status instanceof HTMLElement) {
  form.hidden = false;
  form.addEventListener('submit', event => {
   event.preventDefault();
   const data = new FormData(form);
   const fields = Object.fromEntries([...data].map(([key, value]) => [key, String(value)]));
   const url = composeInquiry(fields);
   if (url.length > 8000) {
    status.textContent = 'ข้อความยาวเกินไปสำหรับร่างอีเมล กรุณาส่งรายละเอียดโดยตรงที่ korvuznox@gmail.com';
    return;
   }
   status.textContent = 'กำลังเปิดแอปอีเมลพร้อมร่างข้อความ หากไม่เปิด สามารถอีเมลถึง korvuznox@gmail.com ได้โดยตรง';
   window.location.href = url;
  });
 }
}
