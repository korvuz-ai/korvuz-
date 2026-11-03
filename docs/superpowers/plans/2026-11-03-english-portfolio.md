# English Portfolio Implementation Plan

Goal: publish the supplied reference's visual direction as a refined English portfolio on the existing Vercel project.

Architecture: static HTML/CSS/JavaScript in `public/`, generated from `site/` by `tools/build-site.py`; no runtime or installation step. Existing GitHub-to-Vercel production integration handles deployment.

Spec: `docs/superpowers/specs/2026-11-03-english-portfolio-design.md`.

- [x] Inspect the reference, canonical resume, active DNS, and deployment.
- [ ] Build the English homepage, standalone details, responsive styles, and accessible interactions.
- [ ] Update routes, metadata, sitemap, snapshot checksums, and repository documentation.
- [ ] Verify English content, local links/assets, dialogs, mobile menu, no-JavaScript behavior, reduced motion, and browser console at desktop/tablet/mobile widths.
- [ ] Review rendered screenshots and accessibility; correct material findings.
- [ ] Obtain an independent code review, push the verified commit to main, and verify the resulting Vercel deployment.
- [ ] Recheck `www` and provide an exact inventory of any old resources that still cannot be retired safely.
