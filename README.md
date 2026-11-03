# Nuntawat Fangritlong — DevOps Portfolio

A personal portfolio for **Nuntawat Fangritlong**, Senior DevOps Specialist in Bangkok. It brings together experience in cloud infrastructure, Kubernetes, infrastructure automation, CI/CD, and systems security.

[Website](https://korvuz.site/) · [Resume](https://korvuz.site/Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf) · [LinkedIn](https://linkedin.com/in/nuntawat-zeo) · [Email](mailto:nuntawat.works@gmail.com)

## Explore the work

- Career experience across enterprise infrastructure and financial services.
- Engineering summaries covering Amazon EKS delivery, infrastructure as code, and RHEL hardening.
- Engineering experience and delivery notes; standalone project pages remain available but are no longer featured on the homepage.
- Practical notes on release readiness, repeatable environments, and security operations.
- The one-page English resume and direct contact information.

The portfolio is entirely in English. Its design follows the supplied portfolio reference, with a midnight and muted lavender palette, clear typography, and responsive layouts.

## Repository structure

| Path | Purpose |
| --- | --- |
| `site/content.json` | Current English career, project, case study, and note content. |
| `site/index.template.html` | Homepage template. |
| `site/icons.svg` | Shared SVG symbols from the supplied reference. |
| `tools/build-site.py` | Dependency-free static site generator. |
| `public/` | Generated HTML, styles, scripts, illustrations, fonts, and PDFs served by Vercel. |
| `source/` | Historical Python/Jinja development source retained from the previous website. |
| `vercel.json` | Static hosting settings, compatibility redirects, and security headers. |

## Build and preview

Requires Python 3.11 or newer. No package installation is needed to generate or serve the site.

```bash
python3 tools/build-site.py
python3 -m http.server 8765 --directory public
```

Open <http://localhost:8765/>. The local server previews the files; Vercel applies hosting redirects and response headers.

Edit the current JSON content and template, rebuild, and commit the updated `public/` files. Styles live in `public/assets/css/portfolio.css`, with the supplied layout foundation in `reference.css`. Interactions live in `public/assets/js/portfolio.js`.

## Deployment

Vercel serves `public/` directly with the **Other** framework preset and installation/build commands disabled. A push to the production branch triggers the connected Vercel deployment. The generated artifact is committed so deployments do not depend on a build runtime.

Case studies, products, and notes have standalone pages. JavaScript adds accessible detail dialogs and an interactive delivery explanation; the content and destination links remain usable without it. Motion respects the user's reduced-motion preference.

## Assets and history

The original resume PDFs keep their established URLs. Product interface illustrations derive from the supplied reference; they represent the products rather than employer systems. Plus Jakarta Sans is self-hosted under its included SIL Open Font License.

The `source/` directory preserves an older development version and its historical deployment records. It is not the generator for the current portfolio. See [the migration guide](docs/VERCEL-MIGRATION.md) for hosting transition details.
