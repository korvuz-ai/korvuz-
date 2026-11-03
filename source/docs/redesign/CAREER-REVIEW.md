# KORVUZ career-first redesign — local implementation and QA

## Scope

Working path: `/opt/korvuz-home`, the main `korvuz.site` source repository. Production continues serving the existing separate versioned release. No deployment, active Nginx configuration, DNS, or `/opt/korvuz-local` changes were made. The only public Local request was a read-only HTTP HEAD to the explicitly supplied destination; it returned **200**.

The eight supplied `ui/01-home.png` through `ui/08-404.png` files guided the new professional layouts. The implementation favors recruiters, hiring managers and professional contacts, with a near-black/indigo palette, local fonts, strong contrast, mobile-first grids, native keyboard navigation, minimal interaction feedback, and static reduced-motion rendering. Primary career pages have no parallax, skill percentage bars, or continuous animation.

## Canonical facts and content mapping

`resume/Senior_DevOps_Specialist.html` is parsed at build time by `tools/career.py`. The shared career record supplies the legal name, professional contact details, six exact employment records and their responsibility bullets, seven skill groups, education/internship details, and source-derived experience label. The primary pages all use this record rather than a second manually maintained employment JSON file.

Current role: **Senior DevOps Specialist — Orbix Custodian — Mar 2026–Present**, exactly as supplied. Employers, dates, outcomes and education were not invented or inferred. No certifications or testimonials were added. The visual reference's unverified commercial offers were not presented as real inventory.

The original PDF files and download URLs remain byte-identical:

- `/Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf`
- `/resume.pdf`
- `/DevOps_Engineer.pdf`

Primary contact details follow the canonical resume: `nuntawat.works@gmail.com`, the supplied phone number, LinkedIn and GitHub. The former `korvuznox@gmail.com` address remains an alternate on Contact and remains intact in original authored content. The contact form prepares an encoded native email draft, validates bounds, rejects recipient/header injection, and explains that the website does not send or store the message. QA did not send an email.

See the [pre-implementation map](CAREER-MAP.md) for the route/content decisions made before implementation.

## Routes and preserved resources

Primary routes are `/`, `/about/`, `/resume/`, `/experience/`, `/skills/`, `/local/`, and `/contact/`. The generated `404.html` provides the eighth reference view with `noindex` and real HTTP 404 responses in the local preview.

Home leads with Nuntawat's professional identity, resume and experience links, a concise career snapshot, and **one small Local teaser**. `/local/` is only a gateway to `https://local.korvuz.site/`; Local's product/commercial details are not mirrored or fabricated here.

All original routes remain available, including `/work/`, all five `/work/{project}/` case studies, `/services/`, `/pricing/` and its calculator, `/blog/` and all six articles, `/lab/`, and consulting compatibility. Original project/media records remain centralized and unchanged; the career redesign intentionally removes the product grid from Home. The six article bodies, authored service terms, pricing data and Lab behavior remain preserved.

Old root hash entrypoints retain query strings and resolve to appropriate surviving pages, including calculator/terminal/stack links. Retired Home work, experience, services, contact, notes and building anchors have useful route destinations. All three consulting entrypoints retain their existing `/services/` 301 behavior and query/fragment preservation. The isolated preview models these existing host redirects; production redirect rules were not changed.

Career page titles/descriptions and structured data now describe the actual person and resume. Existing canonical paths remain unchanged. New Experience/Skills/Local pages have canonical metadata and sitemap entries; the noindex error page and consulting redirect are excluded from the sitemap. Legacy resource/article metadata remains intact.

## Verification

| Check | Result |
| --- | --- |
| Local production build | PASS — 23 canonical pages, consulting compatibility, 404 artifact; 84 files |
| ESLint | PASS |
| Strict JavaScript type checks | PASS |
| JavaScript unit tests | 9 passed, including bounded/encoded professional email drafts |
| Python tests | 35 passed, including canonical facts, data/PDF preservation, media replacement, artifact safety and deterministic builds |
| Full existing desktop browser suite | 41 passed, including calculator, terminal, original PDF downloads, media-editor saves, project image fallbacks, keyboard/no-JS behavior, SEO and accessibility |
| Complete five-width QA | PASS at **320, 375, 768, 1024, 1440px** |
| All-route layout/SEO/image checks | All **115 canonical route/viewport combinations** passed |
| WCAG A/AA axe scans | All 115 canonical route/viewport scans passed with zero violations |
| 404 checks | All 15 path/viewport combinations returned HTTP 404 on GET/HEAD, noindex, valid recovery links and zero accessibility violations |
| Downloads | All three PDFs returned application/pdf and matched their original bytes at every width |
| Local | Exact outgoing URL verified throughout; public HEAD returned 200 |
| Contacts | Canonical email/phone/profile hrefs and encoded email drafts verified at every width; no messages sent |
| Motion/navigation | Static primary pages, reduced motion, native no-JS menu, Enter/Escape/focus return, legacy redirects, consulting 301s and query/hash preservation passed |
| Asset integrity and budgets | PASS; favicon, responsive images, fonts, schema, internal links and required source/download hashes validated |

Machine-readable evidence: [career-validation.json](career-validation.json). Each width has a `qa-{width}.json` and screenshots under [career-preview](career-preview/). The source/download integrity record is [career-preserved.sha256](career-preserved.sha256); build/unit/browser logs are saved beside this report.

Review screenshots: [Home 1440px](career-preview/home-1440.png), [Home 375px](career-preview/home-375.png), [Home 320px](career-preview/home-320.png), [About](career-preview/about-1440.png), [Resume](career-preview/resume-1440.png), [Experience](career-preview/experience-1440.png), [Skills](career-preview/skills-1440.png), [Local gateway](career-preview/local-1440.png), [Contact](career-preview/contact-1440.png), [404](career-preview/404-1440.png).

Browser verification used Chromium at the five requested viewport widths. No claim of deployment or Safari/Firefox testing is made.

## Remaining limitations

- No known local QA regressions remain.
- The four previously unavailable project domains retain their disabled/internal-fallback safeguards. English Reader still has its clearly labeled text cover fallback, and the original gallery arrays are empty. These are retained source limitations on secondary project pages.
- Delivering the designed 404 on a future production deployment needs the optional `deploy/career-404.conf` directive reviewed and included in the existing main-site server block. It was **not installed**, because deployment was prohibited. The custom error page is fully verified in the local preview, with true 404 status rather than a Home catch-all.
- The public site continues to run its previously deployed version until a separate deployment is authorized.

## Local review

```sh
npm run build
python3 tools/preview.py --port 8765 --directory dist
# Separate terminal, if rerunning a complete viewport audit:
node tools/career-qa.mjs --width 375
```

Pre-change local recovery archive: `/tmp/korvuz-career-before/source.tar.gz`. No original PDFs, project data/media records, canonical resume source, article bodies, or Local files were overwritten.
