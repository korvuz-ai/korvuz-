# Korvuz Portfolio Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if the owner explicitly chooses delegation. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a premium freelance portfolio whose real projects, clear offer, mobile usability, and contact path convert prospective clients while retaining existing content and functionality.

**Architecture:** Keep static hosting. Generate pages from shared Jinja2 templates, structured content, and authored HTML using Python; serve small route-specific vanilla JavaScript modules. A local-only media editor writes a shared media manifest and image files; a build optimizes images and produces a separate deployable `dist/` artifact.

**Tech Stack:** Python 3.11+, Jinja2, Beautiful Soup, Pillow, fonttools/Brotli; semantic HTML, CSS, vanilla ES modules; Python unittest, Node 22+ built-in tests, Playwright and Lighthouse for development verification. Public hosting needs only static file serving.

**Spec:** `docs/superpowers/specs/2026-10-15-korvuz-portfolio-redesign-design.md`.

## Global Constraints

- Preserve existing real content, project URLs, blog routes, resume downloads, SEO metadata, and working contact links.
- No fake testimonials, clients, metrics, or content.
- Home order: Hero → Proof → Featured Work → Services → Experience → Process → Pricing teaser → CTA.
- Terminal lives at `/lab/` and is absent from primary navigation.
- The price calculator lives at `/pricing/#calculator`.
- Project images are configured once and reused across Home, Work, and case studies.
- Public pages deliver meaningful HTML without JavaScript; calculator, terminal, and mobile menu are progressive enhancements.
- Image editing is local tooling; saving locally requires a build and deployment to update the public site.
- No deployment, DNS change, or production server reconfiguration occurs without the owner's deployment instruction.

## Review Focus

1. Switching calculator groups must clear hidden options without mixing recurring and one-time prices; tested in Task 6.
2. Real screenshots may be missing, portrait-shaped, or fail at runtime; the image system must preserve layout and show an honest fallback; tested in Tasks 2 and 5.
3. Legacy fragments can be lost during redirects; query strings and rate-specific destinations must survive; tested in Task 8.
4. Media uploads and simultaneous saves can corrupt or escape the local workspace; validation, origin checks, and atomic manifest replacement must prevent it; tested in Task 3.
5. Long Thai text, keyboard navigation, no-JS access, and reduced motion can fail despite a good desktop screenshot; tested in Tasks 4, 7, and 9.

---

## Starting conditions and execution boundaries

The owner approved the direction and requested this specification and plan. Read both documents before implementation; confirm the plan review and execution method at handoff. Native execution is recommended because the tasks share templates, data, and generated routes. No subagents are necessary unless the owner selects them.

This directory is not a Git repository. Do not run Git commits or create a worktree here. At implementation start, create a dated backup outside the served artifact (for example `/tmp/korvuz-redesign-<timestamp>/`) and record a hash manifest. Existing source pages remain intact until migrated output is validated. If the owner later supplies a repository, use that repository's instructions and commit independently verified milestones.

All commands below run from `/opt/korvuz-home`. Tests and build commands are planned commands; they have not been run because their implementation does not exist yet. Dependency versions are to be resolved and locked at implementation, not guessed in this document.

## File map

| Files | Responsibility |
|---|---|
| `requirements-dev.in`, `requirements-dev.lock`, `package.json`, `package-lock.json` | Reproducible build and browser-test dependencies; no public runtime framework |
| `content/site.json`, `projects.json`, `project-media.json`, `pricing.json`, `seo.json` | Shared identity, portfolio, media, prices, and metadata |
| `content/pages/*.html`, `content/blog/*.html` | Trusted migrated content with factual text retained |
| `templates/base.html`, `templates/components/*.html`, `templates/pages/*.html` | Shared shell, media/cards, and page types |
| `assets/css/tokens.css`, `site.css`, `article.css`, `print.css` | Visual system, responsive components, long-form and print layout |
| `assets/js/site.js`, `project-media.js`, `calculator.js`, `pricing-core.js`, `contact.js`, `terminal.js`, `terminal-core.js`, `legacy.js` | Small shared and route-specific enhancements |
| `assets/fonts/`, `assets/projects/<id>/` | Font output and editable raster sources |
| `tools/migrate_content.py`, `build.py`, `content.py`, `media.py`, `check_artifact.py` | Migration, validation, image processing, rendering, and release checks |
| `tools/media_editor.py`, `tools/editor/index.html`, `editor.js`, `editor.css` | Local media editor and bounded save API |
| `tools/__init__.py`, `tests/__init__.py`, `tests/*.py`, `tests/*.test.mjs`, `tests/browser/*.spec.mjs` | Test modules and regression suites |
| `playwright.config.mjs` | Local artifact server and browser test matrix |
| `deploy/nginx-redirects.conf` | Optional host redirect guidance; never auto-applied |
| `docs/redesign/legacy-inventory.json` | Existing read-only preservation baseline |
| `docs/redesign/content-map.md`, `seo-migration.md`, `MEDIA.md`, `DEPLOY.md`, `VALIDATION.md` | Traceable migration, owner workflow, rollout, and actual evidence |
| `dist/` | Generated public artifact; no tools, docs, backups, source JSON, or reference montage |

## Task 1: Preserve and migrate the factual content into a repeatable static build

**Files:** Create dependency manifests, `tools/{__init__,migrate_content,build,content}.py`, `content/*.json`, `content/pages/*.html`, `content/blog/*.html`, minimal `templates/base.html`; `tests/{__init__,test_content,test_build}.py`; `docs/redesign/content-map.md`.

**Interfaces:**
- Consume `docs/redesign/legacy-inventory.json` and the 11 original HTML files.
- Produce `load_content(root: Path) -> SiteContent` in `tools/content.py`; a documented dataclass containing site, projects, media, pricing, SEO, page fragments, and article records.
- Project fields: `id`, `title`, `live_url`, `summary`, `problem`, `solution`, `engineering`, `stack`, `featured`; media is joined by fixed ID. Preserve the configured order InvoiceAI, LineCRM, FiatLine, English Reader, DevOps KB.
- Produce `build_site(root: Path, output: Path) -> BuildReport` in `tools/build.py`, called by `python3 tools/build.py --output dist`; report includes generated routes, copied files, warnings, and bytes.

- [ ] Snapshot current source and verify its hashes against the supplied baseline; fail and reconcile any new owner edits instead of overwriting them.
- [ ] Add failing content tests asserting the five exact URLs from spec §5, all six article slugs, three PDF hashes, every current resume role/date, all consulting terms, and full source-to-destination mapping for every meaningful Home section.
- [ ] Add failing build tests: content is emitted as actual HTML; unknown project IDs, duplicate IDs, absent required SEO, and unsafe live URLs fail; failed build leaves an existing output directory unchanged.
- [ ] Run `python3 -m unittest tests.test_content tests.test_build -v`; confirm failures are missing implementation rather than fixture errors.
- [ ] Resolve and lock development dependencies, implement one-time migration with Beautiful Soup, retain raw baseline metadata, and map trusted article/resume fragments separately from escaped JSON text. Migration is explicit and repeatable, not rerun automatically on every build.
- [ ] Implement content validation and temporary-directory build/replacement. Reject output paths that overwrite source/input directories. Create the documented content map including intentional intro-modal removal and Lab demo separation.
- [ ] Run the same tests and `python3 tools/build.py --output dist`; expect all tests to pass and a valid minimal artifact. Record the milestone without altering production files.

## Task 2: Make project covers and galleries reusable, optimized media

**Files:** Create `tools/media.py`, `templates/components/project_media.html`, `assets/js/project-media.js`, `assets/projects/{invoiceai,linecrm,fiatline,english-reader,devops-kb}/`, `tests/test_media.py`; update media manifest, content validation, build.

**Interfaces:**
- `validate_media(manifest: dict, root: Path) -> MediaManifest` validates schema v1 from spec §6.
- `process_image(source: Path, output: Path) -> ImageVariants` returns width, height, content-hashed fallback and WebP URLs, and srcset entries without upscaling.
- `project_media(project_id, slot='cover')` template macro receives joined media and renders an image or truthful placeholder with stable dimensions.

- [ ] Write tests for a null cover and empty gallery; 1280px source yielding only 480/800/1280 widths; portrait source retaining aspect ratio; missing source being an error; replacement changing hashed filenames; metadata absent from derivatives; traversal/remote source paths rejected.
- [ ] Run `python3 -m unittest tests.test_media -v`; expect failures before implementation.
- [ ] Visually inspect all four existing JPGs. Seed the inspected corresponding covers and document any mismatch; English Reader uses null until a real image is provided. Seed no fictional galleries.
- [ ] Implement the schema, optimizer, and media macro. Use contain by default; fit/focal point are record values. Preserve root image aliases unchanged. Add accessible placeholder text and on-error fallback without frame collapse.
- [ ] Run media and build tests. Build twice and compare artifact hash manifests; expect identical bytes and no upscaled variants. Include a test replacing one cover that proves all generated references resolve to the new image record.

## Task 3: Give the owner a local cover and screenshot editor

**Files:** Create `tools/media_editor.py`, `tools/editor/{index.html,editor.js,editor.css}`, `tests/test_media_editor.py`, `tests/browser/media-editor.spec.mjs`; document `docs/redesign/MEDIA.md`.

**Interfaces:**
- `create_server(root: Path, port: int = 8766) -> HTTPServer` binds only to `127.0.0.1`.
- `GET /api/media` → `{manifest, digest}`; `POST /api/media` consumes `{version: 1, expectedDigest, manifest, uploads}` with header `X-Korvuz-Token`; upload entries identify project ID, slot/gallery ID, and base64 file bytes, never filesystem paths.
- Save returns `{manifest, digest, saved: true}`; errors return `{error, field}` with 400, 403, 409, or 413. The server generates actual source filenames and rewrites references before validation.
- `save_media(root: Path, payload: dict, expected_digest: str) -> SaveResult` validates all changes, writes unique new sources, and atomically replaces the active manifest only after success.

- [ ] Add server tests: valid raster saved and re-readable; bad Origin/Host/token rejected; unsupported/animated raster, spoofed format, 20+MP dimensions, >10MiB image, >50MiB decoded batch, >70MiB JSON body, unknown ID, traversal, and >12 gallery entries rejected without active-manifest mutation; stale digest returns 409.
- [ ] Add failure-injection test: image write or manifest-replace error leaves prior manifest and referenced originals usable. Add caption-escaping fixture containing HTML and quotes.
- [ ] Run `python3 -m unittest tests.test_media_editor -v`; confirm pre-implementation failures.
- [ ] Implement the bounded local server, decoding/validation through Task 2, serialized saves, digest concurrency check, exact local origin/session protection, allowlisted preview serving, and atomic final manifest replacement.
- [ ] Implement cards for all five projects, cover picker, multiple-gallery picker, alt/caption inputs, fit/position, reorder/remove, Save/Discard, previews, and errors. Require alt text before Save. Clearly label unsaved vs saved locally and the separate publish step.
- [ ] Test browser workflow with temporary fixture roots: choose replacement, preview, save, reload; add/reorder/remove gallery; discard leaves disk unchanged; conflict preserves pending edits. Verify error text is visible and no content is injected as markup.
- [ ] Run server tests and `npx playwright test tests/browser/media-editor.spec.mjs`; expect pass. Write short owner instructions: launch, select/edit, save, build, preview, deploy later; include JSON/manual fallback. Ensure the editor is absent from the build output.

## Task 4: Establish the reference-led shared shell and mobile visual system

**Files:** Create `templates/components/{header,footer,seo}.html`, CSS files, `assets/js/site.js`, `assets/fonts/`, `tools/fonts.py`, `playwright.config.mjs`, `tests/browser/shell.spec.mjs`; update base template and site data.

**Interfaces:**
- Base template receives `page: {route, title, seo, active_nav, body_class}`, `site`, and route-specific styles/scripts; has main-content block and skip link.
- `initMenu(root: Document = document): void` and `initReveals(root: Document = document): void` in `site.js` operate safely when their elements are absent.
- `build_fonts(root: Path, output: Path) -> list[Path]` produces local WOFF2 and license notices from the existing Inter/Noto Sans Thai TTF files.

- [ ] Add browser checks: mobile menu initially compact with JS, expands by keyboard, Escape closes and returns focus; menu links remain reachable without JS; no Lab primary link; Resume and Contact remain accessible. At 360px and 200% zoom, no page-level overflow.
- [ ] Add checks that content stays visible when reveal initialization fails and when reduced motion is enabled; sticky header does not cover focused anchors.
- [ ] Run `npx playwright test tests/browser/shell.spec.mjs`; confirm relevant missing-shell failures.
- [ ] Build the shell using spec §3 tokens, spacing, fonts, typography, 1100px initial menu breakpoint, and restrained SVG accents. Use accessible disclosure semantics; avoid a fake modal/drawer role.
- [ ] Implement subtle opt-in reveals, reduced-motion rules, self-hosted fonts, print styles, and shared SEO output. Remove runtime Tailwind and icon-font requirements from generated pages.
- [ ] Run shell tests and visually compare 390px/1440px screenshots against the supplied montage's hierarchy and spacing, without copying its fictional facts or artwork. Record any contrast corrections as token changes.

## Task 5: Deliver the conversion-focused Home, visual Work index, and five case studies

**Files:** Create `templates/pages/{home,work,case_study}.html`, `templates/components/project_card.html`, `tests/test_portfolio.py`, `tests/browser/portfolio.spec.mjs`; update content and build route registry.

**Interfaces:**
- Route registry emits `/`, `/work/`, and `/work/<project-id>/` for exactly the five fixed IDs.
- `project_card(project, variant)` uses variants `featured` and `grid`, consuming the shared media macro and factual project content; distinct case/live anchors, no nested links.
- Home sections carry IDs `top`, `work`, `services`, `experience`, `approach`, `contact` and `data-section` values `hero`, `proof`, `featured-work`, `services`, `experience`, `process`, `pricing`, `cta` in this exact order.

- [ ] Add HTML tests asserting exact section sequence, approved hero headline, three featured stories, two secondary projects, five case-study routes, exact external URLs, and source-backed technical details; empty galleries render no empty section.
- [ ] Add browser tests: screenshot occupies the prominent media panel; null image uses a project-name placeholder; simulated image 404 shows fallback with unchanged bounding height; changing manifest cover updates Home/Work/case after rebuild.
- [ ] Run `python3 -m unittest tests.test_portfolio -v` and the portfolio browser suite; confirm missing-page failures.
- [ ] Implement the Home sequence, large contain-framed screenshots, alternating desktop rows/stacked mobile flow, service/experience/process summaries, exact published teaser rates, and two contact paths.
- [ ] Implement Work and all five case studies from existing factual narratives. Preserve monitoring-vs-uptime nuance and self-built role; do not invent client attribution, duration, or outcomes. Add related-project and inquiry links.
- [ ] Run portfolio tests. Visually inspect at 360/390/768/1024/1440px, checking Thai line breaks, screenshot readability, independent live/case links, and no hover-only actions. Verify content and primary links with JS disabled.

## Task 6: Merge Services and preserve Pricing/calculator behavior

**Files:** Create `templates/pages/{services,pricing}.html`, `assets/js/{pricing-core,calculator}.js`, `tests/pricing.test.mjs`, `tests/test_services.py`, `tests/browser/pricing.spec.mjs`; update pricing data and build.

**Interfaces:**
- Build emits `dist/assets/js/pricing-data.js` exporting data derived from `content/pricing.json`.
- `calculateEstimate(baseId: string, selectedIds: string[], pricing: object): {once: number, monthly: number}` in `pricing-core.js`; IDs are allowlisted and inactive-group options ignored.
- `switchBase(previousBaseId, nextBaseId, selectedIds, pricing): string[]` clears incompatible selections and preserves web selections across Static/WordPress.
- `initCalculator(root: HTMLElement, pricing: object): void` wires native controls to polite status output.

- [ ] Add unit cases: Static no options → `{once:8000,monthly:0}`; all web options → `{once:22500,monthly:2000}`; WordPress all web → `{once:34500,monthly:2000}`; Cloud all options → `{once:44000,monthly:5000}`. Assert Static→WordPress retains web choices; web→cloud→web clears hidden choices; duplicate/unknown option IDs do not inflate totals.
- [ ] Add content checks for all three base inclusions, all consulting sections/FAQs/terms, distinct ฿5,000 maintenance vs ฿15,000–30,000 retainer, and every source-backed price.
- [ ] Run `node --test tests/pricing.test.mjs` and `python3 -m unittest tests.test_services -v`; confirm expected missing-implementation failures.
- [ ] Implement Services sections with `consulting`, `rates`, `hourly`, `audit`, `retainer` IDs. Build Pricing with exact option table, consultation rates, clearly separated recurring pricing, and source wording for estimate limitations.
- [ ] Implement the pure calculation and accessible UI. Preserve the existing inquiry email/subject. With JS disabled, show rates and email rather than a misleading interactive total.
- [ ] Run unit/content tests and `npx playwright test tests/browser/pricing.spec.mjs`; verify group switching, checked-state styling, totals, keyboard input, live summary, mobile layout, and non-JS rates.

## Task 7: Migrate About, Resume, Blog, and Contact without losing evidence

**Files:** Create `templates/pages/{about,resume,blog,article,contact}.html`, `assets/js/contact.js`, `tests/test_migration.py`, `tests/contact.test.mjs`, `tests/browser/content.spec.mjs`; update build, page fragments, CSS.

**Interfaces:**
- Article records: `slug`, `title`, `body_html`, preserved metadata and existing dates; no invented taxonomy.
- `composeInquiry(fields: {projectType?: string, description?: string, budget?: string, timeline?: string}): string` returns URL-encoded `mailto:korvuznox@gmail.com` with factual visitor-entered text, no delivery request.
- `content/pages/resume.html` preserves original meaningful content; `.print-resume` renders through shared print styles and a user-activated `window.print()` button.

- [ ] Add migration assertions: normalized text/headings/tables/FAQ content retained for all six articles and full resume, with only documented link rewrites; three PDF SHA-256 hashes match baseline. About contains actual stack, education, and approach; all old contact destinations remain.
- [ ] Add contact unit cases for Thai text, ampersands, newlines, empty optional fields, and HTML-like input; generated mailto decodes to the original text without extra headers/URL injection.
- [ ] Run `python3 -m unittest tests.test_migration -v` and `node --test tests/contact.test.mjs`; verify failures before implementation.
- [ ] Implement the migrated pages, readable long-form layout, contained table scrolling, correct current-page navigation, inquiry composer with explicit “opens your email app” behavior, and persistent plain email fallback.
- [ ] Implement print treatment: white background, dark text, complete resume content, hidden navigation/buttons, no clipped chronology or blank screenshot pages.
- [ ] Run migration/contact tests and `npx playwright test tests/browser/content.spec.mjs`; check long Thai headings, 200% zoom, article tables, print emulation, plain email without JS, and absence of a message-sent claim.

## Task 8: Move Lab, add compatibility, and reconcile SEO

**Files:** Create `templates/pages/{lab,legacy_consult}.html`, `assets/js/{terminal-core,terminal,legacy}.js`, `tests/terminal.test.mjs`, `tests/test_seo_routes.py`, `tests/browser/legacy.spec.mjs`, `deploy/nginx-redirects.conf`, `docs/redesign/seo-migration.md`; update SEO, build, sitemap, robots output.

**Interfaces:**
- `resolveLegacy(pathname: string, hash: string, search: string): string | null` implements spec §4 allowlisted mapping; returns relative local destination, preserving query before fragment.
- `parseCommand(input: string): {kind: string, argument?: string}` and `resolveProject(alias: string): string | null` in `terminal-core.js` handle legacy aliases; response rendering uses safe DOM text and static trusted templates only.
- Terminal caps history at 100 commands; each submitted command is capped at 1000 characters with visible feedback, without changing other command behavior.
- `tools/check_artifact.py` reports local route/asset/fragment errors, metadata deltas, and preservation exceptions as nonzero exit on unresolved errors.

- [ ] Add command tests for every spec command/alias, unknown input and HTML-like input rendered inert, fixed allowlisted open targets, clear, bounded history, and blocked automatic popup fallback links for resume/projects.
- [ ] Add route tests for every old HTML route, all six article paths, 20 canonical new routes, copied assets, moved hash aliases, and no terminal script on Home. Assert metadata is identical to baseline except enumerated relocation/theme changes; structured data parses.
- [ ] Add browser cases for `/?ref=old#calc` → `/pricing/?ref=old#calculator`, dynamic hashchange, `/#sandbox` → `/lab/#terminal`, `/consult/?ref=old#audit` → `/services/?ref=old#audit`, empty consult fragment → `#consulting`, no-JS compatibility links, and unknown hashes staying put.
- [ ] Run `node --test tests/terminal.test.mjs`, `python3 -m unittest tests.test_seo_routes -v`, and the legacy browser suite; confirm expected missing-feature failures.
- [ ] Implement Lab as an explicitly simulated terminal, preserve commands and static matrix output, label fictional history as demo, avoid unverified operational status, and retain contact/resume functionality. Load its code only on Lab.
- [ ] Implement static compatibility and optional Nginx guidance with the two distinct behaviors specified in §4. Do not apply host config. Rewrite internal links directly to new destinations and preserve ordinary surviving Home anchors.
- [ ] Reconcile per-page metadata against baseline, document each allowed delta, output sitemap/robots, retain OG image and project subdomain entries. Exclude docs/tools/backups/reference montage/source content from `dist/`.
- [ ] Run unit/SEO/legacy tests and the artifact checker; expect all local routes and assets to resolve. Do not claim optional HTTP redirects pass without a configured staging host.

## Task 9: Verify the complete artifact and document publishing/rollback

**Files:** Finish `tools/check_artifact.py`, `tests/browser/accessibility.spec.mjs`, `tests/test_release.py`, `docs/redesign/{DEPLOY,VALIDATION}.md`, `package.json` scripts; update owner media instructions from actual verified workflow.

**Interfaces:**
- `python3 tools/check_artifact.py --root dist --baseline docs/redesign/legacy-inventory.json` exits 0 only when preservation, route, asset, metadata, exclusion, and byte-budget checks pass.
- Playwright config serves only `dist/` at `127.0.0.1:8765`, with Chromium projects for the five required widths; a separate editor fixture uses temporary content and port 8766. No production mutation.
- `npm run audit:mobile` records three repeat Lighthouse mobile runs and medians using the local built artifact; versions/conditions are recorded in validation output.

- [ ] Add release assertions: exact 20 canonical routes, no source-only files, required PDFs/assets hash-identical, no CDN UI runtime, ≤35KiB compressed initial JS and ≤40KiB compressed CSS per route, one eager priority image maximum, build reproducibility, and no public editor/API endpoint.
- [ ] Add accessibility/browser coverage for keyboard-only primary journeys, active navigation, all image alternatives, form labels/status, reduced motion, JS disabled, 200% zoom, focus visibility/header clearance, and no page-level overflow across five widths. Run automated accessibility checks plus manual screen-reader spot checks; do not treat one tool score as full conformance.
- [ ] Run release tests to expose remaining integration failures. Fix the owning template/module rather than weakening preservation expectations.
- [ ] Run `python3 -m unittest discover -s tests -p 'test_*.py' -v`, `node --test tests/*.test.mjs`, `python3 tools/build.py --output dist`, `python3 tools/check_artifact.py --root dist --baseline docs/redesign/legacy-inventory.json`, and `npx playwright test`; record real results and environment limitations.
- [ ] Run the mobile audit and inspect screenshots at 390/1440px against the exact supplied montage. Check real screenshot prominence, first-screen message clarity, project/contact paths, article readability, and editor workflow. Tune only failures or measured performance problems; rerun affected tests.
- [ ] Write `VALIDATION.md` with commands, actual results, artifact manifest/hash, screenshots, lab budgets/scores, known limitations, and unverified host behaviors. Field INP/LCP/CLS remain unmeasured until real field data exists.
- [ ] Write `DEPLOY.md`: deploy only `dist/`; retain an existing release snapshot; preview all canonical and legacy destinations on staging; verify PDF downloads, email drafts, caching, 404s, sitemap, and optional host redirects; explain how to restore the previous artifact/host config. No actual deployment occurs in this task.
- [ ] Present the local artifact, evidence, owner media workflow, and remaining deployment-specific limits for review. Complete authorized reversible fixes before any later deployment approval request.

## Spec coverage map

| Specification | Implementation tasks |
|---|---|
| Outcome, constraints, verified starting point | 1, 9 |
| Reference, visual system, motion, navigation | 4, 5, 9 |
| Route contract, old links, Lab move | 7, 8, 9 |
| Home order and five-second goal | 5, 9 |
| Real work and five case studies | 1, 2, 5 |
| Merged Services and precise Pricing | 1, 6 |
| About, Resume, Blog, Contact | 7 |
| Replaceable covers, galleries, placeholders | 2, 3, 5 |
| Static architecture and reproducible output | 1, 2, 9 |
| SEO/content preservation and compatibility | 1, 7, 8 |
| Mobile, accessibility, no-JS, performance | 4–9 |
| Owner instructions, publishing, rollback | 3, 9 |

## Review and execution handoff

The documents and baseline are review artifacts, not a claim that the redesign exists. The next step is owner review of the spec and plan, then implementation using the chosen method. Recommended: native execution, carrying out Tasks 1–9 in order and reporting meaningful validation milestones. Subagent execution is an alternative only if explicitly selected. No implementation task is marked complete in this plan.
