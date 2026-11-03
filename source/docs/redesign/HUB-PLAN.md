# Korvuz Personal HQ — local rebuild

Scope: `/opt/korvuz-home` only. No deployment, production configuration changes, or work in korvuz-local.

The supplied reference and `ui/cover.png` guide a fresh near-black/deep-purple interface. Home follows Hero → Build/Automate/Operate → Projects → Currently Building/Lab → Experience → Resume Overview → Work With Me → Latest Notes → Contact. Shared navigation, project cards, Work, and case-study presentation use the same new visual system. Original long-form content, SEO, PDFs, contact information, and redirect behavior remain intact.

## Implementation

1. Record source/PDF hashes and archive the pre-change local source.
2. Keep `content/projects.json` as the real project source and join `content/project-media.json` once in the build. No production project backend exists: the existing `/api/media` is a local editing tool only. Extend optional lifecycle/type support without inventing values. Derive internal case-study URLs once. Preserve the four-domain availability override separately from real URLs.
3. Build fresh header, footer, Home, project cards, and shared CSS. Use the supplied artwork as an optimized brand asset, never as a project screenshot. Include all five products; no unverified Lyra/Quant records or invented metrics. The existing simulated Lab is a real experiment surface.
4. Reuse verified resume facts for a concise overview, with full resume and unchanged PDFs one click away. Use existing article records for latest notes and preserve all article bodies.
5. Retain restrained native motion, add Home's new surfaces to reveal/parallax handling, keep desktop parallax ≤6px, disable parallax on mobile, and render static content under reduced motion.
6. Update changed UI contracts in tests. Verify the project cover replacement propagates across Home/Work/case studies, optional statuses, all routes, calculator, terminal, navigation, metadata, assets, keyboard interaction, reduced motion, and no-JS fallbacks.
7. Run local production build, lint, strict JS type checks, JS/Python tests, browser regression checks, and capture desktop/375px screenshots. Report real/fallback data and missing records/media. Do not deploy.

## Known source gaps

- English Reader has no real cover; retain the labeled text fallback.
- All five galleries are empty; render galleries only when real media is supplied.
- No explicit project lifecycle statuses or dated build logs are supplied. Do not infer lifecycle from domain availability.
- Four product domains remain marked unavailable. Preserve original URL records; provide independent disabled Open Product controls and working internal Case Study links.

The source backup is `/tmp/korvuz-hub-before/source.tar.gz`; baseline hashes are `/tmp/korvuz-hub-before/preserved.sha256`.
