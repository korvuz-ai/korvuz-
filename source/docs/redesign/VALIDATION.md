# Release validation — 2026-10-16

Implementation is complete in the static `dist/` artifact. No DNS, production infrastructure, deployment, Git initialization, merge, or push was performed.

## Final verification

| Check | Command / evidence | Result |
|---|---|---|
| Production build | `npm run build` / `python3 tools/build.py --output dist` | 20 canonical pages + consulting compatibility; 74 files |
| Artifact integrity | `python3 tools/check_artifact.py --root dist --baseline docs/redesign/legacy-inventory.json` | PASS: local routes, fragments, assets/srcsets/fonts, schema, image dimensions, release exclusions and byte budgets |
| Python regression suite | `python3 -m unittest discover -s tests -p 'test_*.py' -v` | 27 passed |
| JavaScript logic | `node --test tests/*.test.mjs` | 6 passed |
| Full browser suite before final refinements | `npx playwright test` | 72 passed across six widths |
| Shared Home media / readability release checks | Portfolio, pricing, typography and accessibility browser specs | 30 passed across six widths |
| Final native navigation / page / accessibility checks | `npx playwright test tests/browser/shell.spec.mjs tests/browser/portfolio.spec.mjs tests/browser/accessibility.spec.mjs` | 36 passed across six widths |
| Local image editor | Desktop + 375px replacement/save/reload/reorder/remove/discard; delayed-save lock regression | Passed; included in the full browser suite |
| Optional gallery captions | Temporary build with omitted caption and HTML-like caption | Passed: omitted caption renders; supplied caption is escaped |
| Reproducible build | Two builds compared by SHA-256 manifest | Identical bytes |
| Original content | Baseline hashes plus article/resume/consulting/SEO comparisons | Original source HTML/assets unchanged; retained narratives/metadata match documented migration policy |

Browser verification used Chromium with viewports 360, 375, 390, 768, 1024, and 1440 CSS px. It checks every canonical page for overflow and JS errors, real project hrefs, cover sharing, contain framing, runtime-image fallback without a frame-height change, keyboard menu behavior, Escape/focus return, non-JS navigation/pricing, reduced motion, all PDF downloads, calculator totals/resets/monthly separation, contact email drafts, legacy queries/fragments, print styling, and automated accessibility rules.

The final mobile navigation is a native `details`/`summary` disclosure. A controlled 1.5-second delay of the enhancement script reproduced the original ~0.101 layout shift; the native disclosure fixes it and stays usable with JavaScript disabled. Chromium exposes the summary's native DisclosureTriangle accessibility role, so tests target that semantic HTML element rather than assuming a button tag.

## Mobile Lighthouse lab measurements

Command: `npm run audit:mobile`. Three fresh runs against a loopback server serving the final artifact, after our browser suite stopped. Lighthouse 13.5.0, Playwright/Chromium 1.60.0, Node 22.22.3, Python 3.12.3. Default Lighthouse simulated mobile settings; static local HTTP serving, not production hosting.

| Run | Performance | Accessibility | LCP | CLS |
|---|---:|---:|---:|---:|
| 1 | 98 | 100 | 2.189 s | 0.000007 |
| 2 | 98 | 100 | 2.048 s | 0.000007 |
| 3 | 99 | 100 | 2.049 s | 0.000007 |
| Median | 98 | 100 | 2.049 s | 0.000007 |

All lab targets passed. Concurrent test/audit experiments were retained separately in `test-results/lighthouse-contended/`; their CPU-contended scores are not used as release measurements. Final raw reports and summary are in `test-results/lighthouse/`.

These are local lab results, not production field measurements or marketing claims. Field INP/LCP/CLS, physical-device behavior, Firefox/Safari, actual assistive-technology use, and deployed-host HTTP redirects have not been independently measured. Automated accessibility checks and keyboard/DOM behavior passed; this is not a claim of full screen-reader or WCAG certification. External product destinations are preserved exactly; external uptime was not probed.

## Artifact and budgets

- Manifest SHA-256: `69f47f87dadaef3ec1b79cd7f3b2b325f42be34df63c668dc9d123a8ed891c04`.
- Artifact: 1,831,845 bytes across 74 files, including backward-compatible images and all three original PDFs.
- All CSS across routes: 7,633 gzip bytes (budget ≤40 KiB).
- All JavaScript across routes: 7,140 gzip bytes (stricter than the ≤35 KiB initial-route budget).
- Four local font subsets: 116,268 bytes total; only the critical semibold Latin face is preloaded.
- Only the actual hero/case cover receives high fetch priority; later images are lazy, dimensioned and responsive.
- No runtime Tailwind CDN, icon font, React, animation library, intro modal, or Home terminal code.

## Real content and editable media

All five project records are used on Home, Work and their case studies. Four visually reviewed existing captures seed the covers; English Reader honestly shows “Screenshot coming soon.” Optional galleries are separate and empty until supplied. No testimonials, client logos, fabricated project outcomes or reference-only facts were added.

Use [MEDIA.md](MEDIA.md) for the exact choose → save locally → build → preview → deploy workflow. One record replaces all portfolio surfaces; no component path edits are required. The uploader binds only to loopback and is excluded from the release.

The editor validates actual raster format, size/pixels, IDs/paths, origin/host/token, stale digests and gallery limits; saves are serialized and the manifest replacement is atomic. Browser controls lock throughout file reads and saves. Tests verify failed saves leave the active manifest intact and reject symlink escapes or unrelated build output directories.

## Review decisions and boundaries

A fresh read-only reviewer found two Important issues (save-time editing race and small mobile body type); both were reproduced and fixed. The mobile Home entry was added to satisfy the explicit navigation contract. No deferred review findings remain.

The workspace has no Git repository, so the approved static output/snapshot workflow replaces Git-only worktree/commit operations. Original source snapshot: `/tmp/korvuz-redesign-original-20261015`; durable production backups remain a deployment prerequisite. The unsafe-output regression's local source impact was restored from that snapshot and every original page hash reverified; the builder now refuses source/unrelated output targets.

No production publishing occurred. Default consulting compatibility is static/client-side; optional 301 guidance in `deploy/nginx-redirects.conf` is uninstalled and requires actual-host staging verification. See [DEPLOY.md](DEPLOY.md).

## Visual review artifacts

- [Desktop hero](screenshots/hero-1440.png)
- [375px mobile hero](screenshots/hero-375.png)
- [Tablet Home](screenshots/home-768.png)
- [Featured work](screenshots/work-section-1440.png)
- Key Services, Pricing, InvoiceAI and Contact captures are in `screenshots/` at desktop and 375px.
