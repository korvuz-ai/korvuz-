# SDD ledger — plan: docs/superpowers/plans/2026-10-15-korvuz-portfolio-redesign.md

Approved implementation 2026-10-15. Native execution.
Source snapshot: /tmp/korvuz-redesign-original-20261015.
Ruling: no Git repository exists; use source hashes, local snapshot and a persistent ledger rather than Git-only workflow scripts. No loss of source isolation; release is dist only.
Pre-flight: Tasks 1→2→3 share content/media schema; Tasks 1/2/4→5 share templates and joined media; Tasks 1→6 use exact pricing; Tasks 1/4→7 use migrated fragments; Tasks 1/6/7→8 share route and SEO map; Tasks 1–8→9 produce the artifact. Interfaces consistent.

Tasks 1–8: source migration, media validation/optimization, local uploader, shared templates, 20 pages and compatibility are implemented; integration verification in progress.
Observed and corrected Jinja dict.items attribute collision using explicit service["items"] access.
Task 6 JS tests: 6/6 passing, including calculator group resets, recurring separation, contact encoding, command/redirect contracts.
Task 2 Python media/content checks: 5/5 passing. Task 3 save/conflict/invalid-path checks: 3/3 passing.

Independent final review (read-only agent): no Critical findings; Important save-race and 11px mobile body text reproduced by browser tests then fixed. Save now locks editing during file reads and POST; meaningful Home and article body copy is >=16px, and mobile services use one column. Review regressions: 3/3 passed on 375px. Actual animated WebP rejection and image-failure frame height assertions added.
Final ruling: include explicit Home in the expanded mobile navigation as required by the approved spec; the reviewer called its absence minor because the logo already led Home, but completeness requires implementing it. No added runtime cost of consequence.
Build safety tests: reject source output folders and unrelated external output folders; previous release manifest guards accidental replacement of unrelated files. Original source files restored after the unsafe-path probe and every original page hash reverified.
Performance pass 1: median mobile Lighthouse Performance 92, Accessibility 100; median CLS 0; LCP 2883 ms. Font pipeline reduced from variable subsets (~232 KiB total) to two static weights (~112 KiB total); final audit pending.

Final performance regression: reproduced CLS ~0.101 with delayed menu JS; native details/summary eliminates initial collapse and provides native no-JS operation. Corrected test selectors to reflect Chromium DisclosureTriangle semantics. Final navigation/page/accessibility browser pass: 36/36 across six viewports.
Task 1: complete — implementation and focused/unit/browser verification recorded in VALIDATION.md.
Task 2: complete — implementation and focused/unit/browser verification recorded in VALIDATION.md.
Task 3: complete — implementation and focused/unit/browser verification recorded in VALIDATION.md.
Task 4: complete — implementation and focused/unit/browser verification recorded in VALIDATION.md.
Task 5: complete — implementation and focused/unit/browser verification recorded in VALIDATION.md.
Task 6: complete — implementation and focused/unit/browser verification recorded in VALIDATION.md.
Task 7: complete — implementation and focused/unit/browser verification recorded in VALIDATION.md.
Task 8: complete — implementation and focused/unit/browser verification recorded in VALIDATION.md.
Task 9: complete — build/integrity PASS, 27 Python, 6 Node, prior 72 full-browser and 30 release checks, final 36 browser checks; isolated Lighthouse medians Performance 98, Accessibility 100, LCP 2049.03 ms, CLS 0.000007.
No DNS or production changes; no Git repo to merge/commit. Preserve artifacts and source snapshot for owner review. No deferred reviewer findings.
