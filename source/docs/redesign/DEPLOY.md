# Build, preview, publish, roll back

The redesign is deployed at https://korvuz.site/ through the existing Nginx vhost, using a versioned copy of `dist/`. The original source baseline remains preserved. See [production deployment record](DEPLOYMENT.md) for the active version, durable backup and verified redirects. DNS and TLS settings were not changed.

## Reproduce locally

Python 3.11+ and Node 22.13+ or Node 24+ are development requirements; the public host needs only static files.

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-dev.lock
npm ci
npx playwright install chromium
python3 tools/build.py --output dist
python3 tools/check_artifact.py --root dist --baseline docs/redesign/legacy-inventory.json
npm run lint
npm run typecheck
python3 -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/*.test.mjs
npx playwright test
npm run audit:mobile
```

Preview separately:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8765/`. Use port forwarding when previewing on another computer. Do not serve the full workspace as a release: it contains internal notes, tooling, dependencies and backups.

## Release artifact

`dist/` contains 20 canonical page directories plus `/consult/` compatibility, shared local assets, original image aliases, original OG image and PDF downloads, sitemap, robots, and `release-manifest.json` with SHA-256 values. No hosted upload API is required.

Build output can be the workspace's `dist/` or a separate directory outside the source tree. Output paths that could overwrite source folders are rejected. Rendering/validation happens in a temporary directory; a failed build keeps the previous artifact. Source font files generate self-hosted font subsets once; their embedded license notices are retained.

## Publishing checklist (when deployment is instructed)

1. Identify the actual hosting release directory/configuration; the workspace contains no authoritative deployment pipeline. Do not infer it from DNS.
2. Save a byte-for-byte copy of the currently deployed release and existing server config, including old assets. Keep it outside the public document root.
3. Upload only `dist/` into a new staging/release directory, preserving nested directories and MIME types. Do not upload `node_modules`, editor, source JSON, docs, the montage, or backup files.
4. Serve that directory on staging. Test `/`, `/work/` and all five case studies, `/services/`, `/pricing/`, `/about/`, `/resume/`, all blog routes, `/contact/`, `/lab/`, PDFs, `sitemap.xml`, and `robots.txt`.
5. Test `/consult/#audit`, `/consult/#hourly`, `/#calc`, and `/#sandbox`. The active Korvuz vhost has query-preserving consulting 301s; static compatibility remains in the artifact. `deploy/nginx-redirects.conf` is reference guidance, not automatically applied by builds. Review it against the actual server before installing it.
6. Check that nonexistent paths return 404; never configure SPA catch-all rewrites to Home. Check directory/slashless handling and `/index.html` entrypoints on the actual static host.
7. Confirm mobile navigation, real external project links, native email drafting, resume PDF downloads, calculator monthly separation, and cropped/uncropped project media.
8. Use immutable caching only for content-hashed `/assets/media/` derivatives. Use revalidation/short caching for HTML, unversioned CSS/JS/fonts, sitemap and robots; invalidate relevant CDN caches on release. Do not change DNS for this redesign.
9. Switch the host's release pointer only after staging passes and publishing is authorized. Repeat live read-only smoke checks; do not report local Lighthouse scores as real production field metrics.

## Rollback

Restore the saved previous release directory/release pointer and any changed host config, then clear affected HTML/unversioned-asset caches. Keep original PDFs and project URLs reachable. The development source snapshot is `/tmp/korvuz-redesign-original-20261015` in this session, but `/tmp` is temporary: use a durable release backup before any real deployment. The baseline hashes in `legacy-inventory.json` identify the original source state.

## Owner image updates

Follow `MEDIA.md`: choose a cover/gallery image, save locally, rebuild, preview, then publish the new artifact. Source records, not generated HTML components, are the editing surface.

## Project availability

`content/project-availability.json` controls the temporary public-link fallback for the four unavailable project subdomains. The original URLs in `content/projects.json` remain intact. During a build, unavailable projects lose live buttons, retained authored links and Lab commands route to their internal case studies, and unavailable URLs are excluded from structured navigation and the sitemap. Keep English Reader’s text cover fallback until a real screenshot is supplied. Restore public links only in a later verified release after the domains work.

The current scoped publish helper is `deploy/publish.py`; it checks the saved original-production hash and refuses to overwrite a changed deployment. The active vhost is mirrored in `deploy/korvuz.site.conf`. Next releases must establish a new backup/release record before publishing.
