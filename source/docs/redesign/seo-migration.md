# SEO migration decisions

Baseline: `legacy-inventory.json`. Original metadata is stored in `content/seo.json` and emitted by the shared base template.

Retained on every unchanged canonical route: title, description, author, robots, OG/Twitter facts and image URL, canonical path, structured-data facts, article body/dates/FAQ. `/og-image.png` is byte-identical. All six article routes and three resume PDF URLs remain.

Intentional differences:

- Theme-color changes from cream (where present) to `#09080F` and is added to other pages.
- Character encoding and responsive viewport are emitted once by the shared base template. Old CDN font/Tailwind/icon links are replaced with local assets; they are not SEO copy.
- Home schema's service URLs move from `/#services` to `/services/`; consulting offer URLs move from `/consult/#...` to `/services/#...`. All prices, names, identities, and claims are retained.
- `/consult/` is a legacy compatibility document with canonical `/services/` and `noindex, follow`. It redirects client-side in default static hosting. The original full consulting content and relocated FAQ/service schema are on Services.
- New pages/case studies receive unique descriptions, canonical URLs, OG/Twitter values, and the existing OG asset. Existing page SEO wording is not blanket-rewritten.
- Sitemap adds new canonical pages, removes consulting as a canonical entry, preserves the six article entries, existing old lastmod values and five project-subdomain entries. Newly authored pages have the fixed implementation date; rebuilds do not fabricate new edit dates.
- Default static redirects preserve known old fragments and queries. Optional Nginx 301 guidance preserves incoming fragments by not setting a new fragment. A fragmentless server redirect reaches Services top, where consulting is linked. Host behavior is not claimed until installed/tested on staging.

robots.txt retains the previous allow/disallow rules. Documentation, backups, reference montage, editor, source JSON, tests and tools are excluded from `dist/` independently of robots directives.

Production availability exception (owner-approved deployment): the four NXDOMAIN project destinations are temporarily mapped to internal case-study URLs in structured navigation and authored links, and omitted from sitemap entries. Original source facts and project URLs remain stored unchanged; `content/project-availability.json` records the temporary policy. The active host now serves the consulting compatibility routes with query-preserving 301s.
