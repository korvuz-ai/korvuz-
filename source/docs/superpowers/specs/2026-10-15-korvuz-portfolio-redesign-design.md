# Korvuz portfolio redesign — implementation specification

Date: 2026-10-15
Status: design direction approved; specification and plan prepared for review. No product implementation or deployment authorized by this document alone.

## 1. Outcome and scope

Turn the existing korvuz.site into a premium freelance portfolio and personal studio. Within five seconds a prospective client should understand the offer, find real work, see engineering experience, and know how to make contact.

The approved direction is dark minimal, premium technical, deep black-purple, large typography, spacious layout, subtle purple glow, and restrained motion. It excludes cyberpunk styling. Projects are the main proof; no invented testimonials, clients, logos, metrics, achievements, timelines, availability claims, portraits, or project features.

The owner explicitly requested both this specification and a full implementation plan. Implementation remains a later stage. Keep the public site static; introduce shared build templates and structured content, not a hosted CMS or application framework.

### Global constraints

- Preserve existing real content, project URLs, blog routes, resume downloads, SEO metadata, and working contact links.
- No fake testimonials, clients, metrics, or content.
- Home order: Hero → Proof → Featured Work → Services → Experience → Process → Pricing teaser → CTA.
- Terminal lives at `/lab/` and is absent from primary navigation.
- The price calculator lives at `/pricing/#calculator`.
- Project images are configured once and reused across Home, Work, and case studies.
- Public pages deliver meaningful HTML without JavaScript; calculator, terminal, and mobile menu are progressive enhancements.
- Image editing is local tooling; saving locally requires a build and deployment to update the public site.
- No deployment, DNS change, or production server reconfiguration occurs without the owner's deployment instruction.

## 2. Verified starting point

Workspace: `/opt/korvuz-home`. It contains static HTML, inline Tailwind CDN configuration, Google font links, Font Awesome, and inline JavaScript. No package manifest, build system, hosting configuration, applicable AGENTS.md, or Git repository was found in this workspace. Do not initialize a repository or assume an existing deployment pipeline.

Existing pages: `/`, `/work/`, `/consult/`, `/resume/`, `/blog/`, and six blog articles. The existing home contains experience, stack, work, services, calculator, approach, terminal, contact, a navigation drawer, and a first-visit introduction modal.

Preservation baseline: `docs/redesign/legacy-inventory.json`. It captures all 11 existing pages, source hashes, metadata, head links, structured data, IDs, links, main text, nine image/PDF assets, robots.txt, and sitemap.xml. It was generated from local files; external project availability was not tested.

Existing project images: `invoice.jpg`, `linecrm.jpg`, `fiatline.jpg`, `devops.jpg`, each 1280×800. `invoice.jpg` was visually inspected and is a real InvoiceAI landing-page capture. Review the other three before assigning them as covers. English Reader has no existing dedicated screenshot. Keep the original asset URLs working.

Preserve these PDF bytes and URLs:

- `/Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf`
- `/resume.pdf`
- `/DevOps_Engineer.pdf`

Preserve `/og-image.png` and project image URLs. Backups, internal notes, tooling, media editor, and planning documents must not be shipped in the public artifact.

## 3. Visual reference and design system

The explicit reference is `KORVUZ Dark Portfolio Dashboard Montage.png`, supplied in the workspace and visually inspected. Use its compositional direction: editorial heading hierarchy, dark bordered panels, violet action accents, large product screenshot frames, clear service cards, and restrained technical details. The montage is a design reference, never a source of factual content or a single image used as the website.

Do not reproduce the illustrated raven, generated person, intense light streaks, invented UI screens, fabricated project durations, unsupported prices, or reference-only experience figures. Actual project captures take visual priority. Do not recolor a product UI to make it falsely appear purple.

### Tokens

| Token | Value | Use |
|---|---|---|
| `--color-bg` | `#09080F` | Page background |
| `--color-surface` | `#111019` | Cards, screenshot frames |
| `--color-raised` | `#191623` | Elevated controls |
| `--color-text` | `#F4F1FA` | Primary text |
| `--color-muted` | `#B8B2C7` | Body and secondary text |
| `--color-border` | `#302A3F` | Decorative separators |
| `--color-control-border` | `#776A8D` | Input boundaries requiring contrast |
| `--color-accent` | `#B99AFF` | Links, focus, restrained highlights |
| `--color-button` | `#6840C8` | Primary button with white text |
| `--color-glow` | `rgba(139,92,246,0.10)` | Static ambient gradient |

Verify final composed contrast: normal text ≥4.5:1; large text and meaningful control boundaries ≥3:1. Decorative hairlines do not replace an identifiable input boundary.

Use Inter for Latin and Noto Sans Thai for Thai. Reuse the existing local TTF sources to generate self-hosted WOFF2 assets with a documented font build tool, preserving license notices; allow a system sans-serif fallback. Only preload critical font files; `font-display: swap`. Mono is reserved for small technical labels and `/lab/`.

Use a 4/8px spacing scale; 20px mobile gutters, 32px tablet gutters, 48px desktop gutters; max content width 1200px. Section spacing: 64px mobile, 96px tablet, 120px desktop. Hero heading uses `clamp(2.5rem, 5.8vw, 5rem)`, line height 1.08 with Thai-specific line-height adjustment where needed. Body is at least 16px, line height 1.65. Paragraph measure is at most 68ch. Panel corners 16px; buttons 10px. Do not turn every paragraph into a card.

Hover/focus transitions last 160–220ms. Optional reveal uses opacity and ≤12px translate for 300ms, once. Content starts visible; JS may opt in to animation after successful initialization. Reduced motion disables reveal transforms and smooth scrolling. No continuous particles, parallax, video backgrounds, animated blur, cursor followers, or animation dependency.

## 4. Information architecture and route contract

Canonical routes end in `/`; support slashless paths using the existing host's directory behavior or explicit host redirects.

| Route | Purpose | Source / behavior |
|---|---|---|
| `/` | Freelance conversion page | Existing home, approved sequence |
| `/work/` | All five real projects | Existing work content, visual overview |
| `/work/invoiceai/` | InvoiceAI case study | Existing work project 1 |
| `/work/linecrm/` | LineCRM case study | Existing work project 2 |
| `/work/fiatline/` | FiatLine case study | Existing work project 3 |
| `/work/english-reader/` | English Reader case study | Existing work project 4 |
| `/work/devops-kb/` | DevOps KB case study | Existing work project 5 |
| `/services/` | Unified service scope and consulting | Existing home services + all consult content |
| `/pricing/` | Published rates and calculator | Existing home rates/calculator + consult rates |
| `/about/` | Personal story, approach, full stack | Existing home, resume, approach |
| `/resume/` | Complete experience and printable resume | Existing resume content, unchanged downloads |
| `/blog/` | Existing article index | Existing article titles and dates |
| `/contact/` | Clear inquiry path | Existing email and contact terms |
| `/lab/` | Interactive terminal | Existing terminal, explicitly a simulation |
| `/consult/` | Legacy compatibility page | Permanent redirect to `/services/#consulting` when host supports it |

Case Study is a page type nested under Work, not a redundant empty landing page.

Desktop header: logo → Home; Work, Services, Pricing, About, Blog; Resume text link; prominent “Start a project” → Contact. Use compact menu below the width at which this fits without crowding (initial breakpoint 1100px). Mobile expanded menu includes all those links, Home, and Contact. Case studies are reached through Work. Lab appears only as a small footer link. Keep the header slim, sticky, and clear of focused controls. Use a native disclosure-style mobile menu with button `aria-expanded`, Escape handling, close-on-link, and predictable focus return; do not declare a modal unless implementing modal focus containment.

### Legacy URL compatibility

| Old URL / fragment | Required behavior |
|---|---|
| `/#top` | Home top, retain ID |
| `/#work` | Featured Work, retain ID |
| `/#services` | Home service overview, retain ID, link to full Services |
| `/#experience` | Home experience, retain ID |
| `/#approach` | Home Process, retain legacy ID |
| `/#contact` | Final Home CTA with working email, retain ID |
| `/#stack` | Replace to `/about/#stack` |
| `/#calc`, `/#calcTotal`, `/#calcMonthly` | Replace to `/pricing/#calculator` |
| `/#sandbox`, `/#terminalOutput`, `/#terminalPrompt`, `/#terminalInput` | Replace to `/lab/#terminal` |
| `/consult/` and `/consult/index.html` | `/services/#consulting` |
| `/consult/#rates` | `/services/#rates` |
| `/consult/#hourly`, `#audit`, `#retainer` | Corresponding IDs on Services |
| Any existing `.../index.html` route | Keep serving equivalent page or redirect to its directory URL |

Fragments are not sent to servers. Home gets a small allowlisted `location.replace` mapper on initial load and `hashchange`, preserving query strings. Known moved fragments also have visible fallback anchors linking to their destinations when JS is unavailable. Update internal links to their new intended destinations rather than relying on compatibility code. Do not ship a broad rewrite that returns Home for missing routes.

There are two documented hosting modes:

1. **Default static mode:** `/consult/` and `/consult/index.html` serve a compatibility document. Its script maps known rate fragments to the matching Services ID, maps an empty fragment to `#consulting`, preserves the query, and replaces browser history. It contains a real fallback link and canonical Services URL. This is a client redirect, not an HTTP 301.
2. **Optional Nginx mode:** configure permanent redirects from `/consult` and `/consult/` (and its `index.html`) to `/services/`, without appending a fragment, so browsers preserve an incoming fragment. A fragmentless visit lands at Services top, where consulting is prominently linked. Do not redirect every visit to `#consulting`, which would overwrite `#hourly`/`#audit`/`#retainer`. Verify HTTP status and browser fragment behavior on staging before claiming host redirects work.

Keep IDs `consulting`, `rates`, `hourly`, `audit`, and `retainer` on Services. Pricing uses its own matching rate IDs. The legacy `/consult/` table destination `#consulting` describes default static mode; the optional host mode has the documented top-of-Services difference.

Keep these article routes and body text, dates, headings, tables, FAQs, and related links:

- `/blog/website-price-thailand-2026/`
- `/blog/migrate-to-aws/`
- `/blog/hire-freelance-devops-vs-agency/`
- `/blog/aws-cost-sme-thailand/`
- `/blog/hire-devops-consultant-hourly/`
- `/blog/static-vs-wordpress/`

## 5. Page specifications

### Home

1. **Hero:** approved English headline “Websites, AI tools, and cloud infrastructure—built and shipped.” Supporting Thai copy adapted from the real service descriptions explains responsive websites, LINE/AI workflows, AWS, delivery, and maintenance. Keep Thai as the primary content language with concise English display headings; `lang="th"`, and mark English blocks where appropriate. Primary CTA “View work” → `/#work`; secondary “Discuss a project” → `/contact/`. No modal obstructs first view. Use a real featured screenshot in a restrained frame on desktop and after copy/actions on mobile.
2. **Proof:** concise facts from existing content: Senior DevOps Specialist, experience since 2020, five self-built products, responsibility from code through deployment. Use textual evidence, not client logos or unsupported uptime/revenue/customer figures. No animated counters.
3. **Featured Work:** three substantial image-led stories: InvoiceAI, LineCRM, FiatLine, in that order. At ≥900px, alternate large screenshot/content columns; below, image then text, with no horizontal slider. Each has a real prominent cover, project name, concise problem/solution description, verified stack tags, case-study link, and separate live-product link. Add compact English Reader and DevOps KB entries plus “View all work.” The image is not a CSS background; it has meaningful alt text and a stable aspect ratio.
4. **Services:** web/product delivery, AI and LINE automation, cloud/DevOps, consulting. Only publish deliverables supported by current content. AI/product work without an existing price uses “Scoped after discussion.” Link to Services and relevant Pricing sections.
5. **Experience:** short current-role and earlier cloud/network summary from the actual resume, linked to the full Resume. Keep employment names anonymized as currently shown; do not infer clients from employers.
6. **Process:** adapt the existing consulting workflow: introductory conversation → written scope and price → implementation/review → documented handoff. Preserve existing constraints and avoid inventing generic turnaround promises.
7. **Pricing teaser:** Static from ฿8,000; WordPress from ฿20,000; Cloud/DevOps from ฿15,000. Consulting from ฿1,500/hour with the two-hour minimum adjacent. Link to full inclusions and calculator.
8. **CTA:** “Tell me what you’re building” with email link and contact page; include existing response-time and work-hour wording only in its accurate context.

### Work and case studies

Work shows all five projects in a responsive two-column image-led grid, one column on mobile. No filters are necessary for five projects. Use configured ordering. Projects remain self-built products; never relabel them as paid client engagements.

Each case study: breadcrumb → name and real one-line purpose → main cover → problem → solution and features → engineering decisions/challenges → verified stack and deployment → optional screenshot gallery → live-project link → next project and inquiry CTA. Use ordinary anchors and readable stacked sections, not a complex tab interface. Omit unavailable dates, client names, quantified results, duration, or technology lists. Empty galleries render no heading or empty frame. Additional screenshots use captions, dimensions, and optional links to full-size files; no lightbox is needed.

| ID | Title | Preserve exact live URL | Evidence to retain |
|---|---|---|---|
| `invoiceai` | InvoiceAI | `https://invoice.korvuz.site/` | Thai natural-language invoicing; quotes/receipts; VAT/withholding; Sarabun embedding for Thai PDF; Next.js 14, TypeScript, Gemini API, Prisma/SQLite, Stripe, Docker/Nginx on EC2 |
| `linecrm` | LineCRM | `https://crm.korvuz.site/` | LINE OA customer context, sales pipeline, AI conversation summaries; LINE Messaging API, PostgreSQL, Redis worker queue, Docker Compose |
| `fiatline` | FiatLine | `https://line.korvuz.site/` | Slip OCR, categorization, expense tracking, budgets/savings through LINE; PostgreSQL and background worker |
| `english-reader` | English Reader | `https://en.korvuz.site/` | Short stories, vocabulary context, audio, Thai definitions, matching exercises; do not invent its implementation stack |
| `devops-kb` | DevOps KB | `https://doc.korvuz.site/` | Visualizations, cheatsheets, labs; vanilla JS, zero dependencies; lessons from actual infrastructure work |

Retain the existing shared deployment explanation: Docker isolation, Nginx reverse proxy, Certbot renewals, Grafana/Prometheus host/container metrics. Preserve the explicit distinction that host metrics are not application uptime checks. Use this as engineering context, not a new claim of measured availability. Preserve real roles and facts; qualify current product status as previously described, without displaying an unverified live-status badge.

### Services and Pricing

Services merges the home service inclusions with the complete consulting content: audience and non-fit cases, questions it helps answer, process, FAQs, commercial terms, and related articles. Consulting is a section, not a separate navigation category.

Pricing separates one-time projects, recurring maintenance, and consulting. Keep THB only; the reference's USD toggle is not an implemented requirement. Retain existing scope qualifications and tax wording in their original contexts; do not invent payment or tax terms for other packages.

Calculator rules are unchanged: three bases, mutually exclusive web/cloud option groups, inactive options reset on group switch, Static → WordPress retains web selections, monthly items never inflate the one-time total. Existing add-page/add-revision options are a single checkbox unit; do not silently introduce quantities.

| Base | One-time THB | Group |
|---|---:|---|
| Static | 8000 | web |
| WordPress | 20000 | web |
| Cloud / DevOps | 15000 | cloud |

| Web option | One-time THB | Monthly THB |
|---|---:|---:|
| Additional page | 1500 | 0 |
| Thai + English | 3500 | 0 |
| LINE / chatbot / AI integration | 5000 | 0 |
| SEO + Google Analytics | 3000 | 0 |
| Additional revision | 1500 | 0 |
| Maintenance | 0 | 2000 |

| Cloud option | One-time THB | Monthly THB |
|---|---:|---:|
| Terraform / Ansible | 8000 | 0 |
| CI/CD | 6000 | 0 |
| Monitoring dashboard | 5000 | 0 |
| Autoscaling / HA | 7000 | 0 |
| Additional migration unit | 3000 | 0 |
| System monitoring maintenance | 0 | 5000 |

Consulting: ฿1,500–2,500/hour, minimum two hours; half-day audit ฿6,000–9,000 (~3 hours plus report, with one-hour review); monthly retainer ฿15,000–30,000 for 10/20 hours. The ฿5,000 calculator maintenance option is distinct from the consulting retainer. Preserve advisory vs production-access hourly distinction, free initial 20-minute conversation, one-business-day response wording, evening/weekend scheduling, and explicit lack of 24/7 on-call. Preserve audit deliverables and existing invoicing/payment terms.

Use native labeled radios/checkboxes and an `aria-live="polite"` summary. Provide a non-JS pricing list and email CTA. Keep the existing inquiry subject link; do not require a new backend or fabricated successful submission.

### About, Resume, Blog, Contact, Lab

About uses the real professional summary, stack, engineering approach, education, and journey. Use typography and factual artifacts, not an invented personal portrait. Keep full experience on Resume; preserve all resume text, anonymized employers, education, internship, dates, and downloads. Provide a Print button with usable light print CSS; PDF links remain normal anchors.

Blog preserves all six article bodies and existing metadata; replace page chrome and styling with the shared system, and update moved links. Maintain readable 68ch content, table scroll containers, sequential headings, and visible related articles. Do not invent posts, categories, dates, or search results.

Contact prominently exposes `mailto:korvuznox@gmail.com` and `https://github.com/korvuz-ai`. Use a small optional inquiry composer with project type, description, and budget/timeline as optional fields; it generates a URL-encoded mailto draft and says it opens the visitor's email application. No required personal-data collection or message-sent state. A plain email link remains available without JS. Do not add unverified LINE IDs, social profiles, scheduling URLs, phone numbers, or guarantees.

Lab preserves terminal commands: `help`, `whoami`, `ls`, `open <name>`, `status`, `skills`, `contact`, `resume`, `cv`, `neofetch`, `git log`, `matrix`, `sudo hire korvuz`, `clear`, `exit`, `sudo exit`, and unknown-command feedback. Existing aliases `devops`, `fiatline`, `invoice`, `linecrm`, `crm` remain. Label the terminal as a playful simulation; `status` is a project directory rather than monitoring. Existing fictional `git log` entries must be labeled demo output and never used as portfolio proof. Keep the optional matrix command as static restrained output, no continuous animation. Use text nodes for input echo, an allowlist for destinations, bounded output history, and no input-driven HTML evaluation. Terminal JavaScript loads on Lab only.

Intentionally replace the first-visit intro modal with the unobstructed hero; retire its localStorage key without reading/writing it. Existing navigation behavior is replaced with the accessible shared menu, while its destinations stay reachable.

## 6. Project media and owner workflow

### Source of truth

Store authored project text and ordering in `content/projects.json`; store media references in `content/project-media.json`. Templates consume a joined Project record. Neither Home nor Work embeds a screenshot filename directly.

Media schema version 1:

```json
{
  "version": 1,
  "projects": {
    "invoiceai": {
      "cover": {
        "src": "/assets/projects/invoiceai/cover-source.jpg",
        "alt": "InvoiceAI interface showing Thai invoice creation",
        "fit": "contain",
        "position": "50% 50%"
      },
      "screenshots": [
        {
          "id": "invoice-preview",
          "src": "/assets/projects/invoiceai/invoice-preview-source.png",
          "alt": "Description of the uploaded screenshot",
          "caption": "Owner-authored factual caption"
        }
      ]
    }
  }
}
```

The gallery entry is an interface example, not seed content. Seed actual galleries as empty arrays. Every real project has a record; `cover: null` is valid. IDs are the five fixed project IDs above. Alt text is required for an uploaded image. Position is two percentages from 0 to 100; fit is `contain` or `cover`. Additional screenshots default to contain. A null cover renders a consistent typographic panel with the project name and “Screenshot coming soon,” never a generated product UI or fabricated illustration.

Seed InvoiceAI with the inspected capture. Assign other existing images only after visual review; English Reader initially uses the placeholder unless an actual screenshot is available. Keep existing originals at their root URLs as compatibility assets. The montage is never assigned as a project cover.

### Easy replacement tool

Provide a local-only media editor, launched with `python3 tools/media_editor.py`. It binds to `127.0.0.1` on a configurable port (default 8766) and opens a browser page listing the five projects. It is excluded from `dist/` and has no public admin route.

The owner can choose a cover or multiple screenshots with file inputs, see real previews, write alt text/captions, choose contain/crop and focal position, reorder/remove gallery entries, and click Save. File selection is a preview; Save persists files and JSON into the workspace. The UI distinguishes unsaved changes, saved locally, errors, and “Build and deploy to publish.” It never reports that a local save updated the live site. Discard before save leaves disk unchanged. Removing a reference need not delete its original file; do not perform destructive media garbage collection.

Editor endpoints: `GET /` serves the editor; `GET /api/media` reads the media manifest; `POST /api/media` accepts a versioned JSON update with changed image files encoded as base64 and an expected manifest digest. Successful save returns the new digest. Conflict returns 409 and preserves the unsaved selection for reloading/reapplying. Invalid input returns 400/413 with a field-specific message and no active-manifest change. Limit total decoded upload bytes to 50 MiB/request, 10 MiB/image, 20 megapixels/image, and 12 additional screenshots/project. Accept decoded PNG, JPEG, and WebP only; reject SVG, animated images, malformed images, and misleading extensions. Filenames and project IDs are generated/allowlisted, never used as unchecked paths. Bound JSON request size to 70 MiB before reading it; Pillow validates actual format/dimensions before re-encoding and strips metadata from published derivatives.

Require exact local Host/Origin checks and a per-session unguessable token on mutations to prevent browser-origin attacks on the local editor. Serve only known editor assets and project previews through bounded path resolution. Do not use an unrestricted general-purpose file server. Save new images to unique filenames, validate the whole proposed manifest, then atomically replace the manifest; preserve the previous manifest if any validation/write fails. A second save using an outdated digest is a conflict. Do not trust MIME declarations, captions as markup, or client-provided filesystem paths.

Document a manual fallback: copy a raster into `assets/projects/<project-id>/`, update its one record in `content/project-media.json`, run the build, inspect, then deploy. This supports an owner who does not run the editor. A hosted uploader/account system is outside this redesign.

### Rendering and optimization

`picture`/`img` elements use explicit dimensions, `srcset`, and `sizes`. Produce width variants 480, 800, 1280, and 1600 only up to the original width, with WebP and JPEG/PNG fallback. Use content hashes in generated derivative filenames to avoid stale caches. Preserve image aspect ratio within a 16:10 outer Home/Work frame; contain by default so a screenshot is readable and uncropped. Never upscale a low-resolution source or destructively overwrite an original. Do not eagerly load all five covers or case-study galleries.

The shared `project_card.html` and `project_media.html` templates derive media from the same record. Replacing a cover and rebuilding changes all three surfaces automatically. Missing source file at build is an actionable error; a null cover is a valid placeholder. A runtime image load failure reveals the matching placeholder without changing frame size. Broken images remain visibly diagnosable in build logs.

## 7. Implementation architecture

Use Python 3.11+ for a static build, Jinja2 for HTML templates with autoescape, Beautiful Soup for one-time HTML migration and preservation checks, Pillow for image validation/derivatives, and fonttools with Brotli support for local WOFF2 conversion. These are development tools; no Python executes on the public host. Use vanilla CSS and small page-specific ES modules, no runtime Tailwind CDN, icon font, React, or animation library. Use a small consistent inline SVG icon set.

File ownership:

- `content/site.json`: identity, contact URLs, navigation, footer.
- `content/projects.json`: five source-backed project narratives, IDs, ordering, live URLs, stack.
- `content/project-media.json`: cover/gallery references only.
- `content/pricing.json`: exact existing bases, options, consulting terms.
- `content/pages/*.html`: migrated trusted authored Home/Services/About/Resume/Contact fragments as needed.
- `content/blog/<existing-slug>.html`: unchanged article body text with moved links updated.
- `content/seo.json`: exact legacy metadata plus explicit new-page metadata and relocation mapping.
- `templates/`: base shell, page templates, focused reusable components, SEO output.
- `assets/css/`: tokens, layout/components, article and print rules.
- `assets/js/`: menu/reveals, legacy fragments, calculator, contact composer, terminal (route-specific).
- `assets/projects/<id>/`: source media; root images remain compatibility assets.
- `tools/`: inventory/migration helpers, static build, media processing, local editor, validation.
- `tests/`: preservation, content/media, calculator/terminal and browser regression coverage.
- `dist/`: generated deployable artifact only, never the editing source of truth.

Build command: `python3 tools/build.py --output dist`. Fail on unknown project IDs, unsafe URLs/paths, missing media references, duplicate IDs, missing required content, invalid metadata, and dangling local asset links. Build to a temporary directory then replace the output only after validation so a failure does not leave a partially publishable tree. Repeated builds from unchanged sources produce identical artifact bytes; do not inject timestamps.

HTML pages and links are generated at build time. JavaScript does not fetch project content to create the main page. The calculator reads a build-generated pricing data module derived from `content/pricing.json`. Templates autoescape ordinary content; trusted migrated HTML is a deliberately separate author-only path. Never mark editor captions or imported filenames as safe HTML.

## 8. SEO, content migration, and publishing

Preserve existing titles, descriptions, canonical routes, robots directives, OG/Twitter data, image references, and structured-data facts for unchanged routes. Keep metadata in `content/seo.json` from the baseline rather than retyping it. New pages get unique Thai descriptions and appropriate canonicals. Keep `<html lang="th">` unless a page's actual content changes language.

Relocated content is an explicit exception for URL-bearing metadata: `/consult/` becomes a compatibility document with canonical Services; merge its truthful FAQ/service data into Services and point offer URLs at actual new sections. Home service schema may update URL references to Services/Pricing but must preserve prices, identity, and facts. Document every intentional metadata delta in `docs/redesign/seo-migration.md`; no blanket replacement of existing SEO copy. Theme-color may change from cream to `#09080F` as a documented visual update. Retain `og-image.png` unchanged for this implementation.

Preserve all meaningful original home content through redistribution to the appropriate new pages; preserve resume and article body text except link rewrites. Retain original project descriptions/details in case studies. Intentional removals are UI plumbing (intro modal, old drawer markup, old CSS/CDN scripts) and clearly labeled nonfactual demo output confined to Lab.

Sitemap retains all existing reachable project subdomain entries and article entries, adds new canonical pages/case studies, and removes the redirected consulting page. Preserve accurate old lastmod dates; new pages may use implementation date, not a fresh date on every build. robots.txt retains existing exclusions; add exclusions for internal tooling/docs only if the deployment could expose them. The build must exclude them regardless of robots.

Ship `dist/` for ordinary static hosting plus `deploy/nginx-redirects.conf` as optional reviewed host guidance, not an applied server change. Include all three original PDFs, original project image aliases, OG asset, sitemap, robots, and real page directories. Provide deployment smoke checks, backup/rollback instructions, cache considerations, and an output file manifest. Do not deploy from the entire workspace directory.

## 9. Acceptance and validation

- Five-second manual review: on desktop and mobile, offer, work CTA, and contact path are immediately clear; first screen has no intro modal.
- Home section order matches the global contract; real screenshot panels dominate Featured Work and all five projects are discoverable.
- All 11 old routes remain functional or have the specified compatibility destination; all 20 canonical pages exist (including Home, six original blog pages, and five case studies). Verify route count from the explicit route lists rather than an assumed number.
- All exact project URLs, email links, six article bodies, resume contents, PDF bytes, retained original assets, and intentional metadata differences are checked against the baseline.
- Calculator default is ฿8,000 with no monthly charge; all 12 options retain rates; group-switch resets and shared web selections behave as specified; one-time/monthly values never combine.
- Every terminal command remains reachable on Lab, unknown input is inert text, external destinations are allowlisted, output is bounded, and Home loads no terminal code.
- Editor can replace a cover and add/reorder/remove gallery screenshots; a single saved record controls Home/Work/case study after build. Test null cover, absent gallery, bad file, oversized upload, conflicting save, and runtime image failure.
- At 360, 390, 768, 1024, and 1440px widths, no page-level horizontal overflow; screenshots, Thai headings, tables, and contact address remain usable. Test 200% zoom, keyboard flow, reduced motion, and non-JS access to content and fallback links.
- Target WCAG 2.2 AA: skip link, landmarks, one H1/page, ordered headings, alt text, labels, visible focus, current-page navigation, 44px practical touch targets, contrast, unobscured focus, and status announcements.
- Target production mobile LCP ≤2.5s, CLS ≤0.1, and INP ≤200ms, verified with field data only when available. Prelaunch use three repeat Lighthouse mobile runs on the same local artifact; median Performance ≥90 and Accessibility ≥95 as lab targets, not invented public metrics. Actual field results are not promised by local scores.
- Initial page JS budget ≤35 KiB compressed; CSS ≤40 KiB compressed; mobile first-view media ≤350 KiB; no third-party UI/animation runtime. Load only one priority image when used above the fold; lazy-load later covers/galleries. Font/HTML/image transfer contributes to the page budget report.
- Run local link/asset/schema checks and browser smoke tests; report failures honestly. External links are preserved exactly; any optional read-only external check reports authentication/network failures separately from broken local routing.

## 10. Execution handoff

Implement against the accompanying plan at `docs/superpowers/plans/2026-10-15-korvuz-portfolio-redesign.md`. Recommended method is native execution in this session because shared templates, content migration, and media contracts are tightly connected. Review this spec and plan before implementation. No Git commit was possible because the workspace is not a repository; preserve local snapshots rather than initializing Git without instruction.
