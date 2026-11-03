# Korvuz Personal HQ — local review

Working/source path: `/opt/korvuz-home`. This is the main `korvuz.site` repository, confirmed by `deploy/release.json` and the existing site's Nginx configuration. Production serves a separate versioned release. This task changes only local main-site source and its build; no deployment, DNS, production configuration, or korvuz-local changes.

## What changed

- Fresh Home, header/footer, project cards, Work introduction, and case-study product actions, guided by `ui/korvuz-main-hub-example.png`.
- Home follows Hero → Build/Automate/Operate → Projects → Currently Building/Lab → Experience → Resume Overview → Work With Me → Latest Notes → Contact.
- Near-black/deep-purple design tokens, raven wordmark, supplied `ui/cover.png` artwork, responsive product grid, concise resume summary, verified engineering timeline, real article previews, and a supporting collaboration section.
- Replaced the old shared layout CSS. Removed retired Home process/proof/hero-card styles and motion hooks. Preserved the authored long-form article/resume content and associated typography/print behavior.
- Motion uses requestAnimationFrame only when needed, observes visible timeline geometry, limits desktop pointer offsets to 6px for hero art and 4px for project frames, and preserves image dimensions. Reveals are 250–360ms, interactions 150ms, and native page transitions 120ms. No mobile parallax. Reduced motion disables animations/transitions and uses static content.

## Project source and API inspection

The public main site is a static artifact served by Nginx; it has no production project database or project API. Existing backend inspection found `tools/media_editor.py` with `GET/POST /api/media`, a loopback-only authoring tool over the same real media manifest. That tool is not a public content API. No replacement backend/API was created, and the browser makes no speculative API calls.

Real records remain in **`content/projects.json`**. Real covers and galleries remain in **`content/project-media.json`**. **`tools/content.py:project_records()`** joins them once and adds derived internal case-study URLs and the independent availability flag. `tools/build.py` processes those joined records into responsive media and passes the same records to Home, Work, and every case study.

No project object, cover path, stack, or product URL is hard-coded inside Home. Updating one media record and rebuilding updates all surfaces. Existing local media-editor support is retained.

Optional lifecycle fields accept `live`, `building`, `research`, `experiment`, and `archived`. No current author record specifies a lifecycle; those values remain unset. Home's Building section automatically selects records with `building`, `research`, or `experiment` if real statuses are added later. It currently features only the verified existing simulated Korvuz Lab, explicitly labeled as an experiment.

`content/hub.json` holds Home editorial copy, capability summaries, skills and timeline summaries grounded in the existing resume and supplied `resume/Senior_DevOps_Specialist.html`. It contains no duplicate product records. Note dates/categories/excerpts derive from the original article bodies and `<time datetime>` elements at build time; `content/articles.json` is unchanged.

## Real vs fallback/mock

| Surface | Source | Classification |
| --- | --- | --- |
| Five project identities, descriptions, stack and external URLs | `content/projects.json` | Real, unchanged |
| Four existing project covers | `content/project-media.json` + `assets/projects/` | Real, unchanged |
| English Reader cover | Explicit text-only “Screenshot coming soon” frame | Presentation fallback; no fabricated screenshot |
| Galleries | Five empty author-supplied arrays | Missing media; no mock images inserted |
| Project lifecycle | Optional, absent on all five current records | Unknown; no invented lifecycle |
| Product reachability | `content/project-availability.json` | Existing availability policy, separate from lifecycle |
| Lab | Existing `/lab/` terminal | Real feature; explicitly a simulation, not live server state |
| Hero artwork | Supplied `ui/cover.png` | Brand illustration, not a product screenshot or personal photo |
| Resume, notes, contact | Existing content/PDFs/site configuration | Real, preserved |

No mock project records are used, created, or substituted for real records. No unverified Lyra/Quant entries, testimonials, users, revenue, or production metrics were added. Project/note counts derive from the actual records; the existing resume supports the 5+ years claim.

## Independent actions and missing data/media

- All five projects have working internal Case Study links.
- Open Product is independent. DevOps KB retains `https://doc.korvuz.site/`. InvoiceAI, LineCRM, FiatLine, and English Reader retain their original external URLs in source but have visibly unavailable, non-focusable product controls while the four domains remain unavailable. No broken external navigation is exposed.
- English Reader is still missing a real cover. All five records lack gallery screenshots and explicit lifecycle statuses. No verified additional building/research records or dated build logs were supplied; they are not fabricated.
- All three original PDF bytes and download paths remain unchanged, along with `/resume/`. The supplied resume HTML remains untouched. The legacy raw `resume/index.html` was already absent at task start; tests now compare the public resume against the saved original migration narrative and frozen fragment hash instead.

## Preservation and verification

Preserved: all 20 canonical routes, five case studies, six article bodies, original metadata/structured data, pricing/calculator behavior, contact information/email draft behavior, Lab commands, original PDFs, legacy hash/query routing, and consulting compatibility. Production redirect configuration was not edited. Host-level 301s were not rerun because this is a local-only build.

| Check | Final result |
| --- | --- |
| Local production build | PASS — 20 canonical pages + consulting compatibility, 82 files, 2,164,747 bytes |
| ESLint | PASS |
| Strict JavaScript type checking | PASS |
| JavaScript unit tests | 7 passed |
| Python build/content/media/security tests | 33 passed on frozen source; includes deterministic rebuilds and replacing a single cover across all three surfaces |
| Chromium browser coverage, 1440 / 768 / 375px | 119 unique scenarios passed; 4 intentional desktop-pointer-only skips on tablet/mobile; zero unresolved failures |
| WCAG A/AA axe scans | All 60 route/viewport combinations passed with zero violations after fixes |
| Final focused browser run | 27 passed; verified final typography, all-route overflow/error checks, independent actions, decoded covers, Home/Contact and affected case-study accessibility |
| Final navigation/no-JavaScript/layout-stability rerun | 9 passed across desktop, tablet and 375px; native disclosure, keyboard Escape/focus return, reduced motion and delayed-script stability |
| Artifact preservation/link/schema/media checks | PASS |
| Original project/media/PDF hashes | PASS — byte-identical |
| Compressed budgets | All CSS 9,618 bytes gzip; all JS 9,670 bytes gzip, including route-only modules |
| Screenshots | 1440px, 768px, 375px; every real image decoded before capture |

The browser totals combine unique scenarios from the broad run and final focused rerun. The shared host's long aggregate scans exceeded runner/session limits, so remaining cases were completed separately. A real Contact CTA contrast issue, a lost font token during cleanup, and undersized capability subtitles were corrected and reverified. The merged record uses the latest result for each scenario; it does not claim the earlier interrupted command exited successfully.

Screenshots: [desktop full page](hub-preview/home-1440.png), [375px full page](hub-preview/home-375.png), [tablet full page](hub-preview/home-768.png), [desktop first screen](hub-preview/hero-1440.png), [375px first screen](hub-preview/hero-375.png).

Detailed machine-readable coverage: [hub-validation.json](hub-validation.json). Final artifact identity and byte budgets: [hub-artifact.json](hub-artifact.json). Source integrity evidence: [hub-preserved-data.sha256](hub-preserved-data.sha256). Build, Python, browser and screenshot logs are saved beside this report as `hub-*.log`.

To review locally:

```sh
npm run build
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
# In another terminal, after the preview starts:
node tools/capture-hub.mjs
```

No deployment was performed. Browser verification used Chromium; production infrastructure and live-host redirect behavior were preserved without modification.

Source/PDF hashes: `/tmp/korvuz-hub-before/preserved.sha256`. Pre-change recovery archive: `/tmp/korvuz-hub-before/source.tar.gz`. These are local recovery files outside the public build.
