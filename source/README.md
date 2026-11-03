# KORVUZ — Nuntawat Fangritlong

A career-first personal site for recruiters, hiring managers and professional contacts. Career facts are parsed from `resume/Senior_DevOps_Specialist.html`. The original resume PDFs, project records/media, articles and legacy routes remain preserved. KORVUZ Local stays a separate destination at `https://local.korvuz.site/`; this site provides only a small gateway.

This rebuild is **local only and has not been deployed**. Build `dist/` for review; the root HTML is the migration baseline. See [career content/route map](docs/redesign/CAREER-MAP.md) and [career QA report](docs/redesign/CAREER-REVIEW.md).

## Build and preview

Development tooling requires Node 22.13+ or Node 24+, and Python 3.11+.

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-dev.lock
npm ci
python3 tools/build.py --output dist
python3 tools/check_artifact.py --root dist --baseline docs/redesign/legacy-inventory.json
python3 tools/preview.py --port 8765 --directory dist
```

Open <http://127.0.0.1:8765/>. No framework/server runtime is required by the public artifact.

## Change a project cover or gallery

```bash
python3 tools/media_editor.py
```

Select a real image, add alt text, save locally, then rebuild and preview. The single record updates Work and every case-study surface; galleries remain separate. Career Home intentionally has no project grid. See [image workflow](docs/redesign/MEDIA.md).

## Verify

```bash
npm run lint
npm run typecheck
python3 -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/*.test.mjs
npx playwright install chromium
npx playwright test
npm run audit:mobile
```

Lint covers JavaScript sources, tooling, and browser tests. Type checking uses strict TypeScript `checkJs` on all production enhancement modules; declarations describe the build-generated pricing module and are excluded from the release.

[Production deployment record](docs/redesign/DEPLOYMENT.md) · [Deployment and rollback](docs/redesign/DEPLOY.md) · [SEO migration](docs/redesign/seo-migration.md) · [Validation evidence](docs/redesign/VALIDATION.md)

Do not rerun the one-time `tools/migrate_content.py` importer for normal edits. Edit `content/` records/fragments or use the media editor, then build. No DNS or infrastructure change is required.
