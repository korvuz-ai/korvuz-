# Korvuz — งานต่อ SEO / เว็บ (handoff)

อัปเดตล่าสุด: 2026-08-23 · ไฟล์เว็บหลัก: `/opt/korvuz-home/index.html` (nginx เสิร์ฟตรง = เซฟ = ขึ้นจริงทันที)
สำรองไว้: `/opt/korvuz-home/index.html.bak-2026-08-23` (ย้อนได้ถ้าพัง · ทุกไฟล์ที่แก้ 23 ส.ค. มี `.bak-2026-08-23` คู่กันหมด)

---

## ✅ ทำเสร็จแล้ว (11 ก.ค. 2026)
1. **ส่วนบริการ & ราคา** (`#services`) — การ์ด 3 แพ็กเกจ: Static ฿8,000 · WordPress ฿20,000 · Cloud/DevOps ฿15,000
2. **ตารางคำนวณราคา** (`#calc`) — เลือกประเภท + ออปชันเสริม → ราคารวมอัตโนมัติ
   - ออปชันสลับชุดตามประเภท: Static/WordPress = ชุดเว็บ · Cloud = ชุดงานระบบ (IaC, CI/CD, Monitoring ฯลฯ)
3. **Popup ผลงานตอนเข้าเว็บ** — เด้งครั้งเดียวต่อคน (localStorage), ปิดด้วย X / พื้นหลัง / Esc
4. **Technical SEO** — title+meta description, Open Graph, Twitter card, JSON-LD (Person+Service+ราคา), canonical, robots
5. `/opt/korvuz-home/sitemap.xml` + `/opt/korvuz-home/robots.txt`

---

## ✅ ทำเพิ่ม (26 ก.ค. 2026)
- **แก้ `doc.korvuz.site` ที่ตาย (502)** — container `devops-kb` ถูกลบไป (image ยังอยู่) → `cd /opt/devops-kb && docker compose up -d` กลับมา 200 แล้ว
  มี `restart: unless-stopped` อยู่แล้ว ครั้งหน้า reboot ไม่ตายซ้ำ · ⚠️ ถ้าเจอ 502 อีก เช็ค `ss -ltn | grep 8080` ก่อน
- **ตัดสถานะปลอมออกจาก fake terminal** — เดิม hardcode ว่าทั้ง 4 service `● ONLINE` + latency `12ms/8ms/15ms/11ms` + "All systems operational ✓"
  ทั้งที่ไม่ได้ ping จริง (doc ตายมานานแต่ยังขึ้น 12ms) → ตอนนี้เหลือแค่รายชื่อโปรเจกต์ + โดเมน
  **ห้ามใส่ตัวเลข uptime/latency กลับเข้าไปถ้าไม่ได้วัดจริง** — เว็บขายบริการ DevOps โชว์ตัวเลขปลอม = เสียความน่าเชื่อถือ
- **หน้า hub ผลงานใหม่ `/work/`** — บรรยาย 5 โปรดักต์ + `<a>` จริงไปทุก subdomain + `CollectionPage`/`ItemList` JSON-LD
  ลิงก์เข้าจาก: ปุ่มท้าย section `#work`, footer หน้าแรก, drawer ทุกหน้า (เดิมชี้ `/#work`)
- **บทความเพิ่ม 3 ชิ้น** (รวมเป็น 5) ทุกตัวมี BlogPosting + FAQPage JSON-LD และ cross-link กันครบ
  - `/blog/website-price-thailand-2026/` — ค่าทำเว็บบริษัท ราคาเท่าไหร่
  - `/blog/aws-cost-sme-thailand/` — ค่า AWS เดือนละเท่าไหร่
  - `/blog/hire-freelance-devops-vs-agency/` — จ้างฟรีแลนซ์ vs จ้างบริษัท
- **sitemap** = 13 URL · เช็คแล้วทุกตัวตอบ 200 · ลิงก์ภายในไม่มี 404
- ⚠️ **`en.korvuz.site` = EnglishReader คนละโปรดักต์** ไม่ใช่เว็บเวอร์ชันอังกฤษ → **ห้ามใส่ hreflang จับคู่กับ korvuz.site**
- ⚠️ `/opt/korvuz-home` **ไม่ใช่ git repo** — แก้ไฟล์ = แก้ production สด · backup ล่าสุด `index.html.bak-2026-07-26`
  (ตัว `.bak-2026-07-11` ใช้ย้อนไม่ได้แล้ว เพราะเก่ากว่าเมนู hamburger)

---

## ✅ ทำเพิ่ม (23 ส.ค. 2026) — ราคา consult + resume HTML
- **หน้าใหม่ `/consult/`** — rate card ที่ปรึกษา (คิดเป็นเวลา ไม่ใช่เหมาโปรเจกต์)
  - รายชั่วโมง **฿1,500–2,500** (ขั้นต่ำ 2 ชม.) · ตรวจระบบครึ่งวัน **฿6,000–9,000** · retainer **฿15,000–30,000/เดือน**
  - `Service` + `OfferCatalog` JSON-LD ใช้ `UnitPriceSpecification` + `unitCode: HUR/MON` · มี FAQPage + BreadcrumbList
  - แยกจาก `#services` ตั้งใจ — `#services` = ขายชิ้นงาน, `/consult/` = ขายเวลา · ทั้งสองหน้าลิงก์หากัน
- **หน้าใหม่ `/resume/`** — resume เวอร์ชัน HTML (`ProfilePage` + `Person` JSON-LD ที่มี `knowsAbout` / `alumniOf` / `sameAs`)
  - PDF อย่างเดียว Google จัดอันดับแย่ · หน้า HTML คือตัวที่ทำให้ค้นชื่อ/alias แล้วเจอ · PDF ยังอยู่เป็นปุ่มดาวน์โหลด
  - มี `@media print` — กด Ctrl+P แล้วได้หน้าสะอาดไม่มีเมนู/ฟุตเตอร์
- **บทความที่ 6** `/blog/hire-devops-consultant-hourly/` — เจาะคีย์เวิร์ด "จ้างที่ปรึกษา devops รายชั่วโมง" ลิงก์เข้า `/consult/`
- ต่อ `OfferCatalog` ในหน้าแรกเพิ่ม 3 offer ของ consult + การ์ด teaser ท้าย `#services` + ลิงก์ nav/footer/drawer ทุกหน้า
- **เมนูเป็นอังกฤษทั้งหมดแล้ว** (23 ส.ค.) — ทั้ง nav บนแถบและ drawer ทุกหน้าใช้ป้ายอังกฤษชุดเดียวกัน
  `Home · Work · Consulting · Blog · Pricing · Price calculator · Contact · Resume · Download Resume`
  (หน้าแรกมี `Experience · Stack · Terminal` เพิ่มเพราะเป็น anchor ในหน้าตัวเอง) · aria-label ก็เป็นอังกฤษแล้ว
  ⚠️ **เนื้อหาในหน้ายังเป็นไทยตามเดิม** — เปลี่ยนแค่เมนู · footer ก็ยังเป็นไทย ถ้าจะเปลี่ยนต้องสั่งเพิ่ม
  ⚠️ ป้ายเมนูอยู่ใน **11 ไฟล์** ถ้าจะแก้คำใดคำหนึ่งต้องแก้ให้ครบทุกไฟล์ · backup ก่อนแก้เมนู: `*.bak-menu-en`
- **sitemap = 16 URL** (เพิ่ม 3) · เช็คแล้วทุกตัว 200 · ลิงก์ภายในไม่มี 404 · JSON-LD ทุกหน้า parse ผ่าน

### ⚠️ ค้างอยู่ ต้องตัดสินใจเอง
1. **`/resume.pdf` เปิดสาธารณะและมีชื่อจริง + เบอร์ + อีเมลส่วนตัว + ชื่อบริษัททุกที่** (Krungsri, Mobileconnect, Fujitsu, Tri Petch, Pro Inside)
   Google อ่านข้อความใน PDF ได้ → **อาจโดน index ไปแล้ว เช็คเองด้วย `site:korvuz.site filetype:pdf`** · หน้า `/resume/` ใช้ alias + ปิดชื่อบริษัทตามที่ตกลง (แบบ A)
   ทางเลือกถ้าอยากปิด: ใส่ `add_header X-Robots-Tag "noindex";` ที่ `location ~* \.pdf$` ใน nginx (ยังโหลดได้ แต่หลุดจากผลค้นหา)
2. **`/DevOps_Engineer.pdf` = ไฟล์เดียวกับ `resume.pdf` เป๊ะ ๆ** (md5 ตรงกัน) เปิดสาธารณะซ้ำอีกที่ — ลบทิ้งได้ถ้าไม่ได้ใช้
3. **ไทม์ไลน์ในหน้าแรกขัดกับ PDF** — `#experience` เขียน "ธนาคารชั้นนำของไทย 2022 – ปัจจุบัน"
   แต่ PDF บอก Krungsri = Current และมี Mobileconnect 2024–2025 / Fujitsu 2023–2024 คั่นอยู่ก่อนหน้า
   `/resume/` ยึดตาม PDF (ละเอียดกว่าและไม่ขัดกันเอง) → **ต้องเลือกว่าอันไหนถูก แล้วแก้อีกอันให้ตรง**
4. **resume PDF เก่า** (ไฟล์ลงวันที่ 4 ก.ค. 2026) — ถ้าอัปเดตใหม่ ต้องแก้ `/resume/` ให้ตรงด้วย
5. [ ] request indexing 3 URL ใหม่ใน GSC: `/consult/` · `/resume/` · `/blog/hire-devops-consultant-hourly/`
6. [ ] เอา `/consult/` ไปวางที่ validator.schema.org เช็ค `UnitPriceSpecification` ว่า parse สะอาด
       (Rich Results Test จะไม่ขึ้นอะไร — Service/ราคา ไม่มี rich result ตั้งแต่แรก ไม่ใช่บั๊ก)

---

## 🔲 ต้องทำต่อ (พรุ่งนี้) — ส่วนที่ต้องทำเองบน Google
> ขั้นตอนพวกนี้ Claude ทำแทนไม่ได้ ต้องล็อกอินบัญชี Google เอง

1. [ ] **Google Search Console** → https://search.google.com/search-console
       เพิ่ม property `korvuz.site` → เลือกแบบ **Domain** → ยืนยันด้วย **DNS TXT** (ง่ายสุด เพราะคุม DNS อยู่)
       ⚠️ **ต้องเป็นแบบ Domain ไม่ใช่ URL prefix** — sitemap ของเราลิสต์ URL ข้าม host (`doc.` `line.` `crm.` `en.` `invoice.`)
       ซึ่ง Google จะยอมอ่านก็ต่อเมื่อ host เหล่านั้น verify อยู่ในบัญชีเดียวกัน · แบบ Domain ครอบให้ทีเดียวจบ
2. [ ] เมนู **Sitemaps** → ใส่ `sitemap.xml` → Submit
3. [ ] **URL Inspection** → วาง `https://korvuz.site/` → **Request Indexing**
4. [ ] **Rich Results Test** (https://search.google.com/test/rich-results) → วาง URL → เช็ค Person/Service ขึ้นเขียว
5. [ ] เทสต์แชร์ link ใน LINE/FB → ดูว่าขึ้นรูป + หัวข้อไหม
6. [ ] (ถ้ารับงานในพื้นที่) สร้าง **Google Business Profile** ฟรี

---

## 💡 งานเสริมที่คุยไว้ว่าจะทำต่อ (สั่ง Claude ทำได้)
- [x] ~~ทำรูป **OG image ขนาด 1200×630**~~ ✅ เสร็จ 12 ก.ค. → `/opt/korvuz-home/og-image.png` (live, HTTP 200)
      - เลิกยืม `devops.jpg` แล้ว · `og:image` + `twitter:image` ชี้ไฟล์ใหม่ + ใส่ `og:image:width/height/type/alt`
      - JSON-LD `ProfessionalService.image` ก็ชี้รูปใหม่แล้ว (รูป `devops.jpg` ที่เหลือในหน้า = การ์ดผลงาน ปล่อยไว้ถูกแล้ว)
      - **สร้างรูปใหม่:** `cd /opt/korvuz-home/.tools && python3 make_og.py` (เขียนทับ `og-image.png` ให้เลย)
      - **ถ้าแก้ราคาบนการ์ด ต้องรันคำสั่งข้างบนใหม่** เพราะข้อความ "เริ่มต้น ฿8,000" ฝังอยู่ในรูป → แก้ตัวแปร `label` ใน `make_og.py`
      - เบื้องหลัง: PIL + ฟอนต์ Noto Sans Thai/Inter (เก็บใน `.tools/`) · ต้องมี libraqm ไม่งั้นสระ/วรรณยุกต์ไทยจะเพี้ยน · สี #F7F5F0 / #BC7B4E / #6F8560 ตามเว็บ
- [x] ~~เขียน **บทความ SEO 1–2 หัวข้อ**~~ ✅ เสร็จ 12 ก.ค. — แต่ **ไม่ได้ลง note.korvuz.site**
      - ⚠️ `note.korvuz.site` = แอป **PayXel** (React SPA, `/opt/PayXel/frontend/dist`) ไม่ใช่บล็อก → ลงไม่ได้ + SPA ไม่ดีต่อ SEO
      - ลงที่ **`korvuz.site/blog/`** แทน (static HTML โดเมนเดียวกับหน้าขาย → ลิงก์ส่งพลัง SEO เข้า `#services` ตรง ๆ)
      - `blog/index.html` (สารบัญ) · `blog/static-vs-wordpress/` · `blog/migrate-to-aws/`
      - แต่ละหน้ามี canonical/OG/JSON-LD (BlogPosting + BreadcrumbList) **ของตัวเอง** — ห้ามก๊อป `<head>` หน้าแรกมาทั้งก้อน เดี๋ยว canonical ชี้ผิด
      - ลิงก์จากหน้าแรก: nav (`Blog`) + footer (กันหน้ากำพร้า — ถ้าไม่มีลิงก์ Google ไม่ไต่เจอ)
      - เพิ่ม 3 URL ใน `sitemap.xml` แล้ว
- [ ] **เขียนบทความเพิ่ม** (ยิ่งเยอะยิ่งดี) — ก๊อป `blog/migrate-to-aws/index.html` เป็นแม่แบบ แล้วแก้ title/canonical/og:url/JSON-LD ให้ตรงหน้าใหม่ + เพิ่มการ์ดใน `blog/index.html` + เพิ่ม URL ใน sitemap
- [x] ~~เล็งคีย์เวิร์ด long-tail~~ ✅ ฝังในบทความแล้ว: `รับทำเว็บ static ราคา` (บทความ 1) · `รับวางระบบ cloud aws freelance` (บทความ 2)
- [ ] `รับทำเว็บ wordpress [จังหวัด]` — ยังไม่ได้ทำ ต้องรู้จังหวัดที่จะเจาะก่อน (ทำเป็นบทความ/หน้า landing แยกต่อจังหวัด)

---

## 🍔 เมนู (แก้ 12 ก.ค.)
- เดิมเมนูยัดบนแถบบนหมด (7 ลิงก์) = รก **และมือถือไม่มีเมนูเลย** (nav เป็น `hidden md:flex`)
- ตอนนี้: แถบบนเหลือลิงก์หลักไม่กี่ตัว + ปุ่ม **☰** → กดแล้วแผงเลื่อนเข้าจากขวา (ปิดด้วย ✕ / พื้นหลัง / Esc / คลิกลิงก์)
- ป้าย "open to work · TH" ย้ายไปอยู่ท้ายแผงเมนูแล้ว (เดิมโชว์บนแถบบนตลอด)
- ⚠️ **โค้ดเมนูก๊อปอยู่ 11 ไฟล์แล้ว** (ไม่ใช่ 4 ตามที่เคยเขียนไว้) — `index.html` · `work/` · `consult/` · `resume/` · `blog/index.html` · บทความ 6 หน้า
  ถ้าจะแก้เมนู **ต้องแก้ให้ครบทุกไฟล์** ไม่งั้นเมนูจะไม่ตรงกันระหว่างหน้า
  **หนี้ที่ควรใช้คืนสักวัน:** ย้ายเมนูไปไฟล์เดียวแล้ว include ด้วย nginx SSI (`ssi on;` + `<!--#include virtual="/_partials/drawer.html" -->`)
  ยังไม่ทำเพราะต้องแก้ nginx บนเว็บที่รันจริงและไม่มี git — ถ้าพังคือเว็บล่ม · ทำตอนที่ว่างและมีเวลานั่งเทสต์
  (ข้อดี: ก๊อปบทความใหม่จาก `blog/migrate-to-aws/index.html` จะได้เมนูติดมาเลย)

---

## 📝 หมายเหตุแก้ราคา
- ราคาการ์ด: ค้น `฿8,000` / `฿20,000` / `฿15,000` ใน index.html
- ราคาในตารางคำนวณ: แก้ `value="..."` **และ** ตัวเลข `฿` ในบรรทัด `<span>` ให้ตรงกัน
- ราคาใน SEO: แก้ในบล็อก `application/ld+json` (ช่อง `"price"`) ให้ตรงกันด้วย
- **ราคา consult อยู่ 4 ที่ ต้องแก้ให้ครบ:**
  1. การ์ดใน `consult/index.html` (ตัวเลข `฿` บนการ์ด)
  2. JSON-LD ใน `consult/index.html` (`minPrice`/`maxPrice`)
  3. คำตอบ FAQ ใน `consult/index.html` ที่อ้างตัวเลข (ทั้งใน HTML และใน `FAQPage` JSON-LD)
  4. การ์ด teaser + `OfferCatalog` ใน `index.html`
  (ตาราง "เทียบ 3 ทางเลือก" ใน `blog/hire-devops-consultant-hourly/` ก็อ้างช่วง ฿15,000–30,000 อยู่ด้วย)
- **ไม่ต้องรัน `make_og.py` ใหม่** ถ้าไม่ได้แก้ราคาแพ็กเกจ (฿8,000) บนหน้าแรก — ราคา consult ไม่ได้ฝังอยู่ในรูป OG
