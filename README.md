# KORVUZ — Nuntawat Fangritlong

Personal website and technical writing by **Nuntawat Fangritlong**, Senior DevOps Specialist. My work spans cloud infrastructure, Kubernetes, infrastructure as code, CI/CD, and Linux systems.

[Website](https://korvuz.site/) · [Resume](https://korvuz.site/Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf) · [LinkedIn](https://linkedin.com/in/nuntawat-zeo) · [Email](mailto:nuntawat.works@gmail.com)

## About this repository

This repository brings the website's published files and development source together while preserving the existing Git history.

| Path | Purpose |
| --- | --- |
| `public/` | Exact snapshot of the production website captured on 3 November 2026; the directory configured for Vercel deployment. |
| `source/` | Existing Python/Jinja development source, templates, content, assets, and validation tools. |
| `vercel.json` | Static hosting settings, legacy redirects, and security headers. |
| `docs/` | Migration instructions and SHA-256 checksums for the production snapshot. |

The production snapshot includes the personal homepage, downloadable resumes, and technical articles in Thai. It requires no application server or database.

## Preview the website

```bash
python3 -m http.server 8765 --directory public
```

Open <http://localhost:8765/>. This previews the static files; Vercel-specific redirects and headers are applied by Vercel.

## Deploy with Vercel

Import `korvuz-ai/korvuz-` into Vercel and keep the project root at the repository root. The checked-in configuration uses the **Other** framework preset, skips installation and building, and publishes `public/`.

Test the generated `vercel.app` deployment before connecting `korvuz.site`. Follow [the migration guide](docs/VERCEL-MIGRATION.md) for domain setup, verification, and retiring the previous hosting.

## Development source

The development source produces a different version of the website from the captured production snapshot. Rebuilding `source/` does **not** update `public/` automatically. Review a rebuilt version before promoting its files into the deployment directory.

See [source/README.md](source/README.md) for the existing toolchain and build instructions. Its earlier hosting and deployment notes are historical context; the root `vercel.json` controls the planned Vercel deployment.

## Contact

For DevOps, cloud infrastructure, and technical collaboration: **[nuntawat.works@gmail.com](mailto:nuntawat.works@gmail.com)**.
