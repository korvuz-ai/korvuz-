# Career-first content and route map — before implementation

Scope: `/opt/korvuz-home` only. No deployment, live server configuration/DNS changes, or access to `/opt/korvuz-local`.

Canonical career source: `resume/Senior_DevOps_Specialist.html`, supplied alongside the eight `ui/01-home.png` … `ui/08-404.png` references. Read name, contacts, role titles, employers, exact dates, responsibility bullets, skills and education from that file at build time. Do not substitute the older anonymous Thai resume fragment or the previous Home editorial JSON for these facts. Preserve the original PDF bytes/URLs; do not silently regenerate PDFs from the web layout.

| Existing content | New primary structure | Preservation |
| --- | --- | --- |
| Product-led Home / builder identity | `/`: named professional introduction, resume/experience CTAs, three career domains, small Local gateway | Original products remain `/work/` and all five case studies, sourced from the same real project/media records |
| About fragments / broad role summaries | `/about/`: canonical background, approach, current role and exact six-role journey | Keep `#experience`, `#stack`, `#approach` anchors useful; full details link to dedicated pages |
| Older anonymous resume web fragment | `/resume/`: full canonical professional profile, exact jobs, skills and education | Old fragment retained in source; all three original PDFs remain byte-identical |
| Experience in Home/About/resume | `/experience/`: six roles and dates from canonical resume | No merged/invented employment periods or outcomes |
| Stack in About | `/skills/`: canonical grouped technical skills | No percentage/proficiency bars; no certification claims without source |
| Services/pricing/projects as primary navigation | `/local/`: small gateway to the explicitly supplied `https://local.korvuz.site/` | Do not mirror Local, infer its inventory from a UI mock, or change Local's files. Existing main-site commercial/article routes remain available for SEO/backlinks |
| Project inquiry Contact | `/contact/`: recruiter/professional links and a clearly labeled native email-draft form | Primary email, phone, LinkedIn and GitHub from canonical resume; former public email retained as an alternate contact. No invented backend submission/success message |
| Generic server 404 | `404.html`: designed noindex recovery page with true HTTP 404 in local preview | Preserve real unknown-route status; prepare an optional error-page deployment snippet, never install it |
| Six articles, five project cases, calculator, Lab | Secondary/legacy resources with current canonical paths | Preserve useful real bodies, media, prices, links, downloads and availability safeguards |
| Root hash and consulting redirects | Keep old known redirects and query preservation; map retired Home anchors to useful surviving routes | No DNS, redirect deployment, or catch-all Home fallback |

## Design and implementation

1. Keep a source recovery archive and hashes in `/tmp/korvuz-career-before`.
2. Add a validated parser for the canonical resume; all primary pages share its returned career record. Follow the new eight supplied reference compositions with near-black/indigo tokens, readable type and responsive grids.
3. Use a shared professional header/footer; add Experience, Skills, Local and the 404 artifact. Keep Home's Local section a single small teaser. Do not invent the reference's offers as real product data.
4. Keep the existing static build workflow. Update metadata only for the changed career routes and new pages: accurate personal titles/descriptions, one canonical, Person/ProfilePage schema, noindex 404, and no 404/redirect entries in sitemap. Retain existing canonical metadata on legacy resources.
5. Use native menu and links, labeled/encoded email drafts, keyboard focus, static technical artwork, tiny interaction transitions and reduced-motion support. Primary career pages use no pointer parallax or scroll-driven progress.
6. Update tests whose previous product-led Home/contact contracts are intentionally superseded; preserve independent project/media, pricing, terminal, security and content gates.
7. Freeze product source before final QA. Run production build, lint, strict type checks, JS/Python tests and browser checks at 320/375/768/1024/1440px. Check every route, all PDFs, Local href, contacts, SEO/schema, redirects, real 404 status, no-JS navigation, focus, contrast, reduced motion and assets. Save screenshots and evidence. Do not deploy.

## Known facts and constraints

- Current role: Senior DevOps Specialist, Orbix Custodian, Mar 2026–Present. Previous five roles and all exact dates are present in the supplied resume.
- Canonical email: `nuntawat.works@gmail.com`; LinkedIn: `https://linkedin.com/in/nuntawat-zeo`; GitHub: `https://github.com/korvuz-ai`.
- No certification source is supplied. Do not add certifications. Metrics may only be quoted from the resume and need not be used as decorative statistics.
- Four existing product domains are unavailable. Preserve original record URLs and the existing disabled/internal-fallback policy; the English Reader cover is still a text fallback.
- Custom 404 delivery requires a host error-page directive when deployment is later authorized. This task prepares and locally verifies it without modifying production.
