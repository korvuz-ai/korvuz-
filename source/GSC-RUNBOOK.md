# GSC Runbook — งานที่ต้องกดเอง (26 ก.ค. 2026)

> ## 📌 สถานะล่าสุด — หยุดไว้ตรงนี้ 26 ก.ค. 2026
>
> | ข้อ | สถานะ |
> |---|---|
> | **A** verify korvuz.site แบบ Domain + submit sitemap + request indexing 4 หน้า | ✅ **เสร็จ** |
> | **B** อ่าน 3 ตัวเลขของ invoice.korvuz.site | ✅ **เสร็จ** — sitemap **Success 10 URL** · Pages/Performance **ยังว่างเปล่า** (ปกติของเว็บใหม่ 12 วัน) · request indexing ครบ 5 หน้าแล้ว |
> | **C** Google Business Profile | ⏸️ **ยังไม่ทำ — เริ่มตรงนี้ต่อ** |
> | **D** Rich Results Test | ✅ **ผ่าน** ไม่มี Invalid items · `/work/` ได้ Breadcrumbs + Carousel เป็นของแถม |
>
> **⚠️ FAQ ไม่ขึ้นใน Rich Results Test = ปกติ ไม่ใช่บั๊ก** — Google เลิกโชว์ FAQ rich result ตั้งแต่ ส.ค. 2023
> (เหลือเฉพาะเว็บราชการ/สุขภาพ) หน้าที่มีแต่ FAQPage อย่างเดียวอย่าง `/start` เลยขึ้น "No items detected"
> **ห้ามรื้อ FAQ ออก** — Google ยังใช้อ่านทำความเข้าใจเนื้อหาอยู่ · จะพิสูจน์ว่า markup ถูกใช้ validator.schema.org
>
> ### 🆕 เพิ่มเข้ามา 23 ส.ค. 2026 — ต้อง request indexing 3 URL ใหม่
> `https://korvuz.site/consult/` · `https://korvuz.site/resume/` · `https://korvuz.site/blog/hire-devops-consultant-hourly/`
> (sitemap อัปเดตเป็น 16 URL แล้ว แต่ Google จะไต่เจอเองช้ากว่า — URL Inspection → Request Indexing เร็วกว่า)
> เสร็จแล้วเอา `/consult/` ไปวางที่ **validator.schema.org** เช็ค `UnitPriceSpecification` ว่า parse สะอาด
> ⚠️ **Rich Results Test จะขึ้น "No items detected" สำหรับ `/consult/` = ปกติ** — Service/Offer/ราคา ไม่มี rich result มาแต่ไหนแต่ไร
>
> ### 🔜 ทำต่อวันหลัง เรียงตามผลลัพธ์
> 1. **~3 ส.ค.** กลับมาดู **Pages → Indexed** ว่าขยับไหม + ค้น `site:invoice.korvuz.site` ในเบราว์เซอร์
>    - ยัง 0 → **อย่าเพิ่งเขียนบทความเพิ่ม** ไปหา backlink (ข้อ 2)
>    - ขึ้นแล้วแต่ impressions 0 → เขียนบทความที่ 6–8
> 2. **backlink** ← ตัวที่ขยับเข็มที่สุดตอนนี้ · โพสต์บทความลงกลุ่มฟรีแลนซ์ไทย / Pantip / Blockdit
>    (ยังไม่ได้ร่างโพสต์ไว้ — ขอ Claude เขียนให้ได้)
> 3. **ข้อ C** Google Business Profile (ด้านล่าง)
> 4. *(ไม่ด่วน)* งานเล็กที่รวม build เดียวได้: เพิ่ม `SoftwareApplication` + `BreadcrumbList` ที่ `/start`
>    และเพิ่ม `image` ใน Article JSON-LD ของบทความ InvoiceAI (`app/blog/[slug]/page.tsx`) เพื่อปิด warning

ทำตามลำดับ A → B → C → D · ใช้เวลารวมประมาณ 30 นาที
**บัญชี Google ที่ต้องใช้: korvuznox@gmail.com** (บัญชีเดียวกับที่ verify `invoice.korvuz.site` ไว้แล้ว)

> ⚠️ ต้องอยู่ **บัญชีเดียวกัน** ทั้ง `korvuz.site` และ `invoice.korvuz.site`
> ไม่งั้น sitemap ที่ลิสต์ URL ข้าม host จะไม่ถูกนับ

---

## A · เพิ่ม korvuz.site เข้า Search Console (สำคัญสุด ~10 นาที)

**ทำไมต้องเป็นแบบ Domain ไม่ใช่ URL prefix:** `sitemap.xml` ของเราลิสต์ URL ข้าม host
(`doc.` `line.` `crm.` `en.` `invoice.`) Google จะยอมอ่านก็ต่อเมื่อ host พวกนั้น verify อยู่ในบัญชีเดียวกัน
แบบ **Domain** ครอบทุก subdomain ให้ในทีเดียว — แบบ URL prefix ครอบแค่ `https://korvuz.site/` เท่านั้น

### A1. ขอค่า TXT จาก Google
1. เปิด https://search.google.com/search-console
2. มุมซ้ายบน กดกล่องเลือก property → **Add property**
3. เลือกช่อง **Domain** (ช่องซ้าย ไม่ใช่ URL prefix)
4. พิมพ์ `korvuz.site` (**ไม่ต้องใส่** `https://` และไม่ต้องใส่ `www`) → **Continue**
5. Google จะโชว์ค่าหน้าตาแบบนี้ → **กด COPY**
   ```
   google-site-verification=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   **อย่าเพิ่งปิดหน้านี้ ทิ้งแท็บไว้**

### A2. ใส่ TXT ที่ Cloudflare
1. เปิดแท็บใหม่ → https://dash.cloudflare.com → เลือกโดเมน **korvuz.site**
2. เมนูซ้าย → **DNS** → **Records** → ปุ่ม **Add record**
3. กรอกตามนี้เป๊ะ ๆ:

   | ช่อง | ใส่ |
   |---|---|
   | Type | `TXT` |
   | Name | `@` |
   | Content | วางค่าที่ copy มาจากข้อ A1 (ทั้งก้อน รวม `google-site-verification=`) |
   | TTL | Auto |

4. **Save**
5. รอ 1–2 นาที แล้วเช็คว่าเข้าจริงไหม — เปิด https://dnschecker.org/#TXT/korvuz.site
   ต้องเห็นบรรทัด `google-site-verification=...` (ถ้ายังไม่ขึ้น รออีก 5 นาทีแล้วรีเฟรช)

### A3. กด Verify
1. กลับไปแท็บ Search Console → กด **VERIFY**
2. ขึ้น "Ownership verified" = ผ่าน ✅
3. ถ้าขึ้น failed → รออีก 10 นาทีแล้วกด verify ใหม่ (DNS ยังกระจายไม่ทั่ว) **อย่าลบ record ทิ้ง**

> ❗ TXT record นี้ **ห้ามลบตลอดไป** — ลบเมื่อไหร่ Google ถอน verification ทันที

### A4. ส่ง sitemap
1. ใน property `korvuz.site` ที่เพิ่ง verify → เมนูซ้าย **Sitemaps**
2. ช่อง "Add a new sitemap" → **ต้องพิมพ์ URL เต็ม**:
   ```
   https://korvuz.site/sitemap.xml
   ```
   ⚠️ **Domain property ไม่มี prefix เติมให้** (ต่างจาก URL-prefix property ที่ขึ้น `https://korvuz.site/` ไว้แล้ว)
   ถ้าพิมพ์แค่ `sitemap.xml` เฉย ๆ มันจะไม่ผ่าน
3. **SUBMIT**
4. สถานะ "Couldn't fetch" ในนาทีแรกเป็นเรื่องปกติ — กลับมาดูพรุ่งนี้ ต้องเป็น **Success** และ Discovered URLs = **13**

#### แก้ปัญหาตอน submit

| เห็นอะไร | แปลว่า | ทำยังไง |
|---|---|---|
| ขึ้นแดงทันทีตอนกด Submit | พิมพ์ไม่เต็ม URL | ใส่ `https://korvuz.site/sitemap.xml` ทั้งก้อน |
| **Couldn't fetch** (เพิ่ง submit) | Google ยังไม่ได้ไปดึงจริง | **ปกติ** รอ 1–2 วัน อย่าลบแล้ว submit ซ้ำรัว ๆ |
| **Couldn't fetch** ค้าง 3 วันขึ้นไป | ดึงไม่ได้จริง | กด ⋮ → Remove → submit ใหม่ 1 ครั้ง |
| **Success** แต่ Discovered = 0 | ยังไม่ได้อ่านเนื้อใน | รออีก 1–2 วัน ตัวเลขจะขึ้นเอง |
| ไม่เจอเมนู Sitemaps | ยังอยู่ property เก่า | เช็คกล่องเลือก property มุมซ้ายบนว่าเป็น `korvuz.site` (ไม่มี https:// นำหน้า = Domain property) |

> ✅ ฝั่งเซิร์ฟเวอร์เช็คแล้วปกติ: ดึงด้วย Googlebot UA ได้ **200** · `Content-Type: text/xml` · ทั้ง `http→https` และ `www` เข้าถึงได้หมด
> ฉะนั้นถ้าติด = ติดที่ฝั่ง GSC ไม่ใช่ที่เว็บ

### A4.5 · แล้วมันทับกับ property `invoice.korvuz.site` เดิมไหม?

**ไม่ทับ และไม่ต้องลบอันเก่า** — GSC ออกแบบมาให้ property ซ้อนกันได้

- Domain property `korvuz.site` **ครอบทุก subdomain** รวม `invoice.` `doc.` `line.` `crm.` `en.`
- ฉะนั้นข้อมูลของ invoice จะโผล่ **ทั้งสองที่** = ซ้อนกัน แต่ไม่ตีกัน ไม่มี penalty ไม่ใช่ duplicate
- **ควรเก็บ property `https://invoice.korvuz.site` ไว้ต่อ** เพราะดูตัวเลขเฉพาะ InvoiceAI ได้สะอาดกว่า
  (property รวมจะเอาทุก subdomain มาปนกันหมด)
- sitemap ก็คนละไฟล์ ไม่ทับกัน:
  - `korvuz.site/sitemap.xml` = 13 URL (เว็บหลัก + บล็อก + หน้าแรกของแต่ละ subdomain)
  - `invoice.korvuz.site/sitemap.xml` = 11 URL (หน้าภายในของ InvoiceAI) ← submit ไว้ที่ property ของ invoice เหมือนเดิม
- URL `https://invoice.korvuz.site/` ที่อยู่ใน sitemap ของ korvuz.site **ตอนนี้ถูกต้องแล้ว** —
  เพราะพอ verify แบบ Domain มันอยู่ในขอบเขตเดียวกัน (ก่อนหน้านี้ Google เมินบรรทัดนั้นทิ้ง)

### A5. ขอ index หน้าใหม่ 4 หน้า
เมนูซ้าย **URL Inspection** → วางทีละอัน → รอสแกนเสร็จ → กด **REQUEST INDEXING**
(ทำได้วันละไม่กี่ครั้ง ถ้าโดนจำกัดให้ทำต่อวันถัดไป)

```
https://korvuz.site/work/
https://korvuz.site/blog/website-price-thailand-2026/
https://korvuz.site/blog/aws-cost-sme-thailand/
https://korvuz.site/blog/hire-freelance-devops-vs-agency/
```

---

## B · อ่าน 3 ตัวเลขของ invoice.korvuz.site (~5 นาที)

สลับ property เป็น **`https://invoice.korvuz.site`** แล้วจดค่า 3 ตัวนี้:

| # | ไปที่เมนู | จดอะไร |
|---|---|---|
| 1 | **Pages** (ใต้ Indexing) | ตัวเลข **Indexed** = กี่หน้า |
| 2 | **Sitemaps** | สถานะ = Success / Couldn't fetch |
| 3 | **Performance** → ช่วง Last 3 months | **Total impressions** = เท่าไหร่ |

### แล้วดูว่าตกกรณีไหน

**กรณีที่ 1 — Indexed = 0 หรือน้อยมาก (1–2 หน้า)**
→ ปัญหาคือ Google ยังไม่ยอมเก็บ ไม่ใช่ปัญหาคอนเทนต์
สิ่งที่ต้องทำ: URL Inspection → Request Indexing ทีละหน้า + **หา backlink**
โพสต์บทความลงกลุ่มฟรีแลนซ์ไทย / Pantip / Blockdit พร้อมลิงก์กลับ (ฟรีและได้ผลจริงที่สุดตอนนี้)
**อย่าเพิ่งเขียนบทความเพิ่ม** — เขียนไปก็ไม่ถูกเก็บอยู่ดี

**กรณีที่ 2 — Indexed ≥ 5 แต่ impressions = 0**
→ ถูกเก็บแล้วแต่ไม่ติดอันดับคำไหนเลย = ปัญหาคอนเทนต์/คีย์เวิร์ด
สิ่งที่ต้องทำ: เขียนบทความที่ 6–8 (ตอนนี้มี 5 แล้ว) จับคำยาวเฉพาะเจาะจง

**กรณีที่ 3 — impressions > 0 แล้ว**
→ เริ่มติดแล้ว 🎉 ไปที่ Performance → แท็บ **Queries** ดูว่าคนค้นคำไหนแล้วเจอเรา
แล้วเขียนบทความเจาะคำนั้นเพิ่ม (คำที่ impressions เยอะแต่ CTR ต่ำ = โอกาสที่ชัดที่สุด)

> ⚠️ ค้น Google ว่า "ใบแจ้งหนี้" แล้วไม่เจอเรา = **ปกติมาก** ไม่ใช่บั๊ก
> เว็บใหม่ไม่มีทางชนะคำกว้างที่ FlowAccount/PEAK ยึดมา 10 ปีใน 6 เดือนแรก
> ถ้าจะทดสอบให้ค้น `site:invoice.korvuz.site` — ขึ้นผล = ถูก index แล้ว

---

## C · Google Business Profile (~10 นาที — เฉพาะ korvuz.site)

ทำได้เพราะเป็นธุรกิจบริการ · **InvoiceAI เป็น SaaS ทำไม่ได้** = แต้มต่อที่มีเฉพาะโดเมนนี้

1. เปิด https://business.google.com → **Add your business**
2. ชื่อธุรกิจ: `Korvuz` · ประเภท: `Website designer` (หรือ `Computer consultant`)
3. **เลือก "I deliver goods and services to my customers"** แล้ว **ไม่ต้องแสดงที่อยู่** (บริการออนไลน์ ไม่ต้องเปิดบ้านให้คนมา)
4. พื้นที่ให้บริการ: เลือกจังหวัดที่รับงาน (เลือกได้หลายจังหวัด)
5. ใส่เว็บไซต์ `https://korvuz.site` + เบอร์ติดต่อ
6. ยืนยันตัวตน (Google ส่งโปสต์การ์ด/วิดีโอ แล้วแต่ระบบให้)
7. verify ผ่านแล้ว → ใส่รูป (ใช้ `og-image.png` ได้) + คำอธิบายบริการ + ราคาเริ่มต้น

---

## D · เช็คของฟรีที่ควรทำครั้งเดียว (~5 นาที)

- [ ] https://search.google.com/test/rich-results → วาง `https://korvuz.site/blog/website-price-thailand-2026/`
      ต้องเจอ **FAQ** และ **Article** ขึ้นเขียว
- [ ] https://search.google.com/test/rich-results → วาง `https://korvuz.site/work/` → ต้องเจอ **Breadcrumbs**
- [ ] https://developers.facebook.com/tools/debug/ → วาง `https://korvuz.site/work/` → กด Scrape Again ดูว่ารูปขึ้น
- [ ] แชร์ลิงก์ `https://korvuz.site/work/` เข้า LINE ตัวเอง ดูว่าขึ้นรูป + หัวข้อถูก

---

## ✅ เช็กลิสต์สรุป

```
[ ] A1  copy ค่า TXT จาก GSC (แบบ Domain)
[ ] A2  ใส่ TXT ที่ Cloudflare (Type=TXT, Name=@)
[ ] A3  กด VERIFY → Ownership verified
[ ] A4  Submit sitemap.xml
[ ] A5  Request Indexing 4 หน้าใหม่
[ ] B   จด 3 ตัวเลขของ invoice.korvuz.site มาบอก Claude
[ ] C   สร้าง Google Business Profile
[ ] D   Rich Results Test + FB Debugger + ลองแชร์ LINE
```

**ข้อ B คือข้อที่ปลดล็อกงานรอบหน้า** — ตัวเลข 3 ตัวนั้นตัดสินว่าจะเขียนบทความเพิ่ม หรือไปหา backlink ก่อน
