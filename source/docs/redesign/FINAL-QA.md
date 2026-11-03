# Final Korvuz QA — 2026-10-16

The local production artifact is `dist/`. No deployment, DNS, production-host configuration, merge, or push was performed.

## Changes

- Fixed the malformed Website / WordPress option in Contact. All six project-type options now work and the selected value is included in the email draft.
- Fixed screenshot clipping on desktop hover: parallax moves the full media frame by at most 4px, without scaling or cropping the contained screenshot. Hero parallax remains capped at 6px per axis.
- Inset project/hero image-link focus rings so rounded overflow containers cannot clip them.
- Added the existing Korvuz mark as an explicit SVG favicon. Fresh Lighthouse visits no longer request a missing default favicon or log its 404.
- Added reproducible ESLint and strict TypeScript `checkJs` commands. DOM guards cover forms, inputs, image fallback, navigation, and motion; type declarations describe generated pricing data without shipping them.
- Simplified calculator state without changing amounts, monthly separation, or selection behavior. Documented development requirements and QA commands.
- Expanded regression coverage to every canonical page for accessibility, metadata, missing assets, console errors, and overflow. Added cover-framing, contact-option, original-fragment, and real cover-replacement checks.

## Cleanup

Removed obsolete reveal keyframes, superseded CSS/mobile font/grid rules and transitions, redundant calculator previous-base state/argument, the unused direct Node typing dependency, and eight verified unreferenced backup copies:

- `index.html.bak-gh`
- `index.html.bak-2026-09-12`
- `index.html.bak-2026-07-11`
- `index.html.bak-menu-en`
- `DevOps_Engineer.pdf.bak-2026-09-12`
- `resume.pdf.bak-2026-09-12`
- `sitemap.xml.bak-2026-08-23`
- `sitemap.xml.bak-2026-07-26`

Each removed backup was absent from production and preservation requirements, unreferenced by source/docs, and matched its archived bytes. Temporary recovery archive: `/tmp/korvuz-final-qa-source-backup.tar.gz`. The two HTML backups referenced by `SEO-TODO.md` remain.

Generated Python bytecode caches and obsolete failure traces were cleared; fresh QA reports and refreshed review screenshots remain. No unused production component or asset was removed speculatively. Original source baselines, font sources/licenses, the design reference, all public legacy asset URLs, PDFs, project cover sources and gallery support remain. No placeholder bitmap is shipped; the no-cover/error text fallback is required and retained.

CSS cleanup preserved 21 computed-style comparisons: seven main pages at 1440px, 768px and 375px. Headings, body typography, padding, margins, gaps and grid columns match their pre-cleanup values.

## Routes and media preserved

- Main routes: `/`, `/work/`, `/services/`, `/pricing/`, `/about/`, `/resume/`, `/blog/`, `/contact/`, `/lab/`.
- Case studies: `/work/invoiceai/`, `/work/linecrm/`, `/work/fiatline/`, `/work/english-reader/`, `/work/devops-kb/`.
- All six existing article URLs, narratives, dates, canonical metadata and retained structured-data facts.
- `/consult`, `/consult/`, `/consult/index.html` retain query-preserving static/client compatibility with Services. Known `#rates`, `#hourly`, `#audit`, `#retainer` fragments survive; unknown fragments fall back to `#consulting`.
- `/index.html` and root moved fragments: `#stack`, `#calc`, `#calcTotal`, `#calcMonthly`, `#sandbox`, `#terminalOutput`, `#terminalPrompt`, `#terminalInput`. Existing Home section anchors remain.
- All three original PDF URLs and byte-identical resume downloads; all four original image aliases, OG image, robots and sitemap preservation rules.
- Local slashless requests return 301 with query strings retained; unknown paths return a real 404. Optional Nginx guidance remains uninstalled.

`content/project-media.json` remains the sole cover/gallery record. All five Home cards, Work cards and case studies share that record, including the no-cover case. An isolated rebuild replaced InvoiceAI's central cover source and alt text and verified the same new media URL on the Home hero, Home card, Work card and case study. Editor save/reload/reorder/remove/discard and save-time locking checks pass. Production project data/media records were not edited.

## Final results

| Check | Result |
|---|---|
| `npm run lint` | PASS — JavaScript sources, tooling and browser tests |
| `npm run typecheck` | PASS — strict JS type checking, no emitted runtime files |
| Python/CSS syntax | PASS — 18 Python files and all production/editor stylesheets parsed |
| JavaScript unit tests | 7 passed |
| Python unit/integration tests | 28 passed, including original-content hashes, deterministic builds and cover replacement |
| Full interaction/accessibility browser suite | 59 passed, 4 intentional desktop-only skips at 1440px / 768px / 375px |
| Final favicon/metadata/assets/contact/image follow-up | 7 passed, 2 intentional desktop-only skips at the same widths |
| Accessibility | All 20 canonical pages passed automated WCAG A/AA rules at all three widths |
| Production build | PASS — 20 canonical pages plus consulting compatibility, 77 release files |
| Artifact validation | PASS — routes, fragments, assets, responsive media, schema, dimensions, exclusions and compressed budgets |
| Production dependency audit | No vulnerabilities |
| Lighthouse median | Performance 98, accessibility 100, best practices 100, SEO 100 |
| Lighthouse LCP / CLS median | 2.120s / 0.000007 |

All three final Lighthouse console audits passed; the favicon 404 was eliminated. Lighthouse used simulated mobile settings and a local static server after browser work stopped. These are lab measurements, not production field metrics.

Animation probe: zero scheduled JavaScript frames while idle and zero long tasks during 90-frame scroll samples at every width. Median frame interval was 16.7ms throughout; p95 was 33.4ms desktop and 16.8ms tablet/mobile. This is a headless local sample, not a physical-device/GPU guarantee. Reduced-motion content stays static, mobile parallax is disabled, and native page transitions remain 120ms.

All-route compressed JavaScript: 9,513 bytes. CSS: 8,540 bytes. Manifest SHA-256: `b9d7ee3aaa45b95c249d6538d915a6043cd4ff39c7e3fd443c29ebc7802d11b5`.

Evidence: [full browser log](../../test-results/final-qa/browser-full.log), [final asset checks](../../test-results/final-qa/browser-final-assets.log), [Python](../../test-results/final-qa/python-tests.log), [JavaScript](../../test-results/final-qa/javascript-tests.log), [animation probe](../../test-results/final-qa/animation.json), [Lighthouse summary](../../test-results/lighthouse/summary.json). Refreshed desktop/tablet/375px captures are in `screenshots/`.

## Remaining issues and limits

- Public DNS returned NXDOMAIN (Google DNS status 3, also failing local resolution) for `invoice.korvuz.site`, `crm.korvuz.site`, `line.korvuz.site` and `en.korvuz.site`. Their existing project URLs were preserved; no DNS changes were authorized. `doc.korvuz.site`, GitHub and the AWS calculator destination responded successfully.
- English Reader has no supplied cover screenshot. Its honest text fallback remains until a real capture is added through the centralized media workflow.
- Actual-host redirects, cache/MIME configuration and field performance require staging/live verification when deployment is authorized. Server-side 301 guidance was not installed. No SPA catch-all or DNS changes were made.
- Browser automation covered Chromium at the requested three widths. Safari/Firefox, physical devices and full assistive-technology evaluation were not independently tested.
