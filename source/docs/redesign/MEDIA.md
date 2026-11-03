# Update project covers and case-study screenshots

One media record drives Home, Work, and the project's case study. The main cover and optional case-study screenshot list are separate. No component edits are needed.

## Browser workflow

From `/opt/korvuz-home`:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-dev.lock
python3 tools/media_editor.py
```

Open the printed `http://127.0.0.1:8766/` address on the same computer. If working on a remote machine, use an SSH local port forward with the same local port (for example `ssh -L 8766:127.0.0.1:8766 user@your-server`); do not expose the editor on a public interface. The tool is intentionally absent from the public build.

1. Find the project. Choose/replace its main cover. Pick a real PNG, JPEG, or WebP screenshot.
2. Add meaningful alt text. **Contain** shows the full screenshot; **Cover** intentionally crops it. Use the horizontal/vertical focal-point sliders only when cropping is wanted.
3. Optionally add case-study screenshots. Give each alt text and an optional factual caption. Move up/down or remove entries independently of the main cover. Maximum: 12 additional images/project.
4. Click **Save changes locally**. This writes source images into `assets/projects/<project-id>/` and updates `content/project-media.json`. It does not publish. Discard/reload abandons unsaved choices. A conflict means another save changed the source: retain your pending files, reload, and reapply.
5. Rebuild and validate:

```bash
python3 tools/build.py --output dist
python3 tools/check_artifact.py --root dist --baseline docs/redesign/legacy-inventory.json
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

6. Inspect `http://127.0.0.1:8765/`, `/work/`, and `/work/<project-id>/`. The same replacement should be visible on all three surfaces. Check desktop and 375px mobile.
7. Publish only the `dist/` artifact through your approved deployment process. See `DEPLOY.md`. Changing local files does not change the live site.

Limits: 10 MiB/source image, 20 megapixels/image, 50 MiB decoded uploads/save; static PNG, JPEG, WebP only. SVG/animated images are rejected. New uploads are re-encoded with generated filenames, and published derivatives omit source metadata. If normalized output is too large, reduce the screenshot dimensions before retrying. Source files are not destructively garbage-collected when a record is removed.

## Manual fallback

- Copy a raster into `assets/projects/<project-id>/`.
- Edit only that project's record in `content/project-media.json`.
- `cover` has `src`, `alt`, `fit` (`contain` or `cover`), `position` (`50% 50%` by default).
- `screenshots` is an array with unique `id`, `src`, `alt`, optional `caption`, `fit`, `position`.
- Set `cover` to `null` for an honest project-name placeholder; use `screenshots: []` for no gallery. Missing configured files fail the build rather than silently publishing broken images.
- Run the same build/preview/deploy steps above.

Project IDs: `invoiceai`, `linecrm`, `fiatline`, `english-reader`, `devops-kb`.

Sources are optimized into content-hashed WebP/JPEG size variants without upscaling. Original compatibility URLs such as `/invoice.jpg` stay unchanged; new portfolio panels use the central manifest's generated variants. A runtime image failure reveals the matching placeholder without collapsing the panel.

Do not run `tools/migrate_content.py` to update images: that is the one-time legacy importer and will reset content/media seeds. Normal builds and the editor never rerun migration.
