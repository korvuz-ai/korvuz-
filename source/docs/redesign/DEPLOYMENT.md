# Korvuz production deployment

Deployed successfully to **https://korvuz.site/**. Live smoke completed at **2026-10-16T03:03:01.787Z**. No rollback was required.

## Version and rollback

- Version: `20261016T025158Z-b28ca2a45277`.
- Production document root: `/opt/korvuz-releases/20261016T025158Z-b28ca2a45277`.
- Public manifest: <https://korvuz.site/release-manifest.json>.
- Manifest SHA-256: `b28ca2a452773d20cbc31af33b08b7dece4b1a55ceb39a7d3f7a496c57b3bb41`; the public bytes match the staged artifact.
- Durable private rollback point: `/opt/korvuz-backups/20261016T025158Z`.
- Backup contains the complete pre-deployment production tree (15,368 archived files; 57,636,246 compressed bytes), exact previous Nginx vhost, checksum record, and rollback script. Original public Home, sitemap, robots and all PDFs were verified against the archive before publication.
- Archive SHA-256: `d87b0ebb72a32cf461f0b365a4a6674b8dd08cc413e2822619370bc132a1d961`.

Rollback command, if needed:

```bash
sudo sh /opt/korvuz-backups/20261016T025158Z/rollback.sh /opt/korvuz-backups/20261016T025158Z
```

The script restores the exact previous vhost and validates/reloads Nginx. The original source/baseline root remains at `/opt/korvuz-home`; the full archive is retained for file recovery. `deploy/publish.py` also automatically restores that configuration and verifies the original public Home hash if activation or live smoke fails.

## Existing hosting workflow used

Production was already served directly by the local Nginx vhost for `korvuz.site` and `www.korvuz.site`; public Home bytes matched its original document root before changes. No separate CI/cloud publishing pipeline was present.

Only the approved `dist/` artifact was copied into a root-owned versioned release. The existing vhost now points to that directory, with query-preserving consulting 301s and explicit cache revalidation for mutable assets. Content-hashed project images are immutable. Existing inherited security headers, TLS/Certbot settings, HTTP-to-HTTPS redirects, and unrelated virtual hosts were preserved. Nginx syntax validation passed before its graceful reload and again after publication. The service is active.

No DNS, TLS, cloud resources, unrelated infrastructure, or unrelated host configuration was changed. Development files, source records, tooling, package metadata and docs now return 404 from the public artifact.

## Unavailable projects handled

`content/project-availability.json` records the four temporarily unavailable projects. Original project URLs and media records remain untouched.

- Home and Work live-demo buttons for InvoiceAI, LineCRM, FiatLine and English Reader are hidden; their case-study navigation remains available.
- Their case studies show a short unavailable-demo note with the normal inquiry action.
- Retained Resume project links route to internal case studies.
- `/lab` project commands use build-generated destinations and open internal case studies for these projects. `open invoice` was exercised on the live site at both widths.
- Structured navigation and sitemap entries no longer expose the four unavailable subdomain URLs.
- DevOps KB's available live URL remains active.
- English Reader's text cover fallback remains as explicitly approved.

Restore public demo links only in a later verified release once the domains work.

## Verification results

- `npm run lint` and `npm run typecheck`: passed.
- Production build: 20 canonical pages plus consulting compatibility, 78 files; artifact validation and staged file-hash verification passed.
- Unit/content tests: 30 Python and 7 JavaScript tests passed, including unavailable-link gating, original-content/media preservation and deterministic rebuilding.
- Preflight smoke: 1440px desktop and 375px mobile passed all 20 canonical routes and interactive journeys against the exact staged manifest.
- **Live smoke:** both widths passed Home, Work, all five case studies, Services, Pricing/calculator, About, Resume, Blog plus all six articles, Contact and `/lab`.
- Live PDFs: all three original downloads returned 200, correct PDF MIME and byte-identical files.
- Live favicon, robots and sitemap: 200, correct bytes; SVG MIME verified. Canonical URLs and descriptions were verified on all 20 pages.
- Every project image decoded successfully at both widths; English Reader's fallback remained visible. No horizontal overflow, script exceptions, console errors or failing page resources were found.
- Calculator: base values, web/cloud options, monthly separation and group resets passed. Contact: all six project types and the selected type in email-draft composition passed; no email was sent.
- Mobile navigation: native disclosure, keyboard opening, Escape closing and focus return passed.
- Motion: bounded desktop hero parallax and static reduced-motion behavior passed on the live site. The approved CSS/JS modules are unchanged except the scoped terminal destination update.
- Additional live accessibility: the changed Work, Resume and four unavailable case-study pages passed automated WCAG A/AA rules at both widths (12 scans, zero violations).
- HTTPS `www` alias serves the same approved manifest.

Evidence: [live smoke](../../test-results/deploy-live/smoke.json), [live accessibility](../../test-results/deploy-live/accessibility.json), [desktop screenshot](../../test-results/deploy-live/home-1440.png), [375px screenshot](../../test-results/deploy-live/home-375.png), [preflight](../../test-results/deploy-preflight/smoke.json). Version metadata is also in `deploy/deployment-result.json`.

## Live redirects verified

- `http://korvuz.site/...` → the same path/query on HTTPS, 301.
- `http://www.korvuz.site/...` → the same path/query on HTTPS www, 301; HTTPS www serves the release.
- `/consult`, `/consult/`, `/consult/index.html` → `/services/`, 301, retaining query strings.
- Consulting `#audit`, `#hourly`, `#retainer` and `#rates` survived server redirects in a browser.
- `/work?ref=smoke` → `/work/?ref=smoke`, 301.
- Legacy `/?ref=smoke#calc`, `/index.html?ref=smoke#stack`, and `/#sandbox` reached their Pricing, About and Lab destinations with the expected query/fragment.
- Unknown routes return 404, with no SPA catch-all.

## Remaining issues

No production regression was found by the live checks. The four demo domains remain unavailable, with all public navigation protected by the approved fallback policy. English Reader still has no supplied screenshot and retains its approved text cover. Browser smoke used Chromium at the requested widths; physical devices and other browser engines were not independently tested in this deployment.
