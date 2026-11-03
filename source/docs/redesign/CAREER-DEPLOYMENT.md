# Career-first production deployment

- Production: https://korvuz.site/
- Version: `20261016T131127Z-6edb9a08adfd`
- Approved artifact SHA-256: `6edb9a08adfdca89cccc8716d6817895dbc3898eb0ec45d4dbbe9c5b178dce57`
- Active release: `/opt/korvuz-releases/20261016T131127Z-6edb9a08adfd`
- Verified rollback archive/configuration: `/opt/korvuz-backups/20261016T131127Z`
- Completed: 2026-10-16T13:16:16.814Z

## Deployment

Used the existing versioned-release / Nginx workflow. The previous immutable release remains available. A private full production archive was compared against its original tree, the previous Nginx configuration was saved, and original PDFs were verified unchanged. The existing vhost now points to the approved release and serves its custom error page with a genuine HTTP 404 and noindex metadata. DNS, certificates, and KORVUZ Local files/configuration were unchanged.

The first attempt automatically rolled back after Chromium reported a skipped native transition during rapid mobile automation. Previous public homepage bytes were verified after rollback. The smoke harness now allows the site's 120ms transition to settle before the next navigation or motion-preference change, and includes diagnostic locations for every console error. No console errors were suppressed, and no site artifact changes were needed. The second deployment and full live smoke passed.

## Final live results

- All 23 canonical routes passed at desktop 1440px and mobile 375px, including all five case studies, six articles, career pages, Services, Pricing and Lab.
- Mobile menu Enter/Escape/focus return, calculator totals and resets, professional email draft encoding, contact destinations, Lab internal product fallbacks, and English Reader placeholder passed.
- All three PDFs matched the approved original bytes; favicon, robots and sitemap matched the artifact.
- SEO title/description/canonical, image decoding, overflow, browser console/network/script errors and static reduced-motion rendering passed.
- HTTP main/www to HTTPS preserve paths and queries; HTTPS www serves the same release. Consulting bare/slash/index routes return 301 to Services preserving queries; browser fragments and legacy calculator/stack/terminal/work/experience entrypoints resolve correctly. Slashless Work redirects correctly.
- Custom 404 passed GET and HEAD for unknown routes, `/404/` and direct `/404.html`; source-only paths are inaccessible.
- Live WCAG A/AA scans: 16 page/viewport combinations, zero violations, including contrast and the custom 404.
- Every directly served artifact file (81) matches its release-manifest hash. The manifest itself also matches the approved SHA-256.
- Public Local gateway read-only HEAD returned 200. No messages were sent from Contact.
- Fresh deployment-tool validation: lint, type checks and 9 JavaScript unit tests passed. The deployed artifact is identical to the production build previously verified at 320/375/768/1024/1440px.

## Remaining source limitations

Four unavailable project subdomains remain hidden or routed to internal case studies, with original project records preserved. English Reader retains its approved labeled placeholder cover; original galleries are empty. No known production regressions remain. Browser verification used Chromium; Safari/Firefox were not newly tested.

## Evidence

- [Live smoke](../../test-results/deploy-live/smoke.json)
- [Live accessibility](../../test-results/deploy-live/accessibility.json)
- [Live integrity](../../test-results/deploy-live/integrity.json)
- [Desktop screenshot](../../test-results/deploy-live/home-1440.png)
- [375px screenshot](../../test-results/deploy-live/home-375.png)
- [Release record](../../deploy/deployment-result.json)

Rollback command (requires host privileges): `sudo sh /opt/korvuz-backups/20261016T131127Z/rollback.sh /opt/korvuz-backups/20261016T131127Z`.
