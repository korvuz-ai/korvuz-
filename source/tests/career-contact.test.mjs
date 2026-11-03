import test from 'node:test';
import assert from 'node:assert/strict';
import {composeProfessionalInquiry} from '../assets/js/career-contact.js';

test('professional draft uses canonical recipient and safely encodes user input',()=>{
 const message='DevOps & cloud\nสวัสดี\n<script>alert(1)</script>\nBcc: example@example.com';
 const url=new URL(composeProfessionalInquiry({name:'A & B',email:'reply@example.com',topic:'Job opportunity',message},'nuntawat.works@gmail.com'));
 assert.equal(url.pathname,'nuntawat.works@gmail.com');
 assert.equal(url.searchParams.get('subject'),'KORVUZ / Job opportunity');
 assert.ok(url.searchParams.get('body').includes(message));
 assert.equal(url.searchParams.has('bcc'),false);
 assert.equal(url.searchParams.has('cc'),false);
});
test('recipient header injection and oversized drafts are rejected',()=>{
 assert.throws(()=>composeProfessionalInquiry({},'a@example.com\nBcc:other@example.com'));
 assert.throws(()=>composeProfessionalInquiry({message:'x'.repeat(5001)},'nuntawat.works@gmail.com'));
 assert.equal(new URL(composeProfessionalInquiry({},'nuntawat.works@gmail.com')).protocol,'mailto:');
});
