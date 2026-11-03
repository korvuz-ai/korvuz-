# Vercel migration

## Deployment configuration

Import `korvuz-ai/korvuz-` as a new Vercel project:

| Setting | Value |
| --- | --- |
| Root Directory | Repository root |
| Framework Preset | Other |
| Install Command | Empty; overridden by `vercel.json` |
| Build Command | Empty; overridden by `vercel.json` |
| Output Directory | `public` |
| Environment variables | None required for this static artifact |

The deployment serves the captured production files directly. Python and Node.js are not required to build this migration snapshot. Do not change the output to the repository root: development source and internal documentation are outside the public artifact.

The checksums in `production-snapshot.sha256.json` describe the original 56-file snapshot. Subsequent intentional edits to `public/` should update that record.

## Verify the Vercel deployment

- Open the homepage and confirm the current name, title, layout, and links.
- Check `/blog/` and each of the six article pages.
- Download each of the three resume PDF files.
- Confirm CSS, JavaScript, fonts, images, favicon, `robots.txt`, and `sitemap.xml` load.
- Check a nonexistent path returns HTTP 404 with the custom error page.
- Check `/blog` redirects to `/blog/` and nested article URLs open directly.
- Check `/consult`, `/consult/`, and `/consult/index.html` retain the legacy redirect to `/services/`. The captured production snapshot does not contain a services page, so that destination currently returns 404; restoring one is a separate content decision.
- Confirm query parameters and browser fragments survive relevant redirects.
- Confirm security headers match the checked-in configuration.

The canonical URLs intentionally remain `https://korvuz.site/` while testing on the temporary Vercel domain.

## Connect the domain

1. Save the existing DNS records and their TTL values.
2. Add both `korvuz.site` and `www.korvuz.site` in the project's **Settings → Domains**.
3. Configure `www.korvuz.site` to redirect to `korvuz.site`, preserving the existing canonical hostname.
4. Update only the relevant apex and `www` DNS records to the values Vercel provides for this project. Preserve mail records and other subdomains.
5. Wait for valid domain configuration and HTTPS, then repeat the verification on the production domain.

There is no requirement to transfer the domain registration or move all DNS hosting to Vercel.

## Retire the previous hosting

Keep the previous S3/CloudFront setup available during the DNS transition. Retain it for at least 48–72 hours and longer if the original DNS TTL or verification requires it.

Before deleting anything:

- Confirm the production domain serves Vercel from more than one network.
- Keep an independent copy of the source and the previous production artifact outside the VPS.
- Confirm no remaining page or download depends on S3 or the VPS.
- Check other services before removing anything from the VPS. Korvuz Atlas and other subdomains have a separate lifecycle.

Then disable and delete the old website's CloudFront distribution, empty/delete its S3 bucket including object versions where applicable, and remove only the obsolete website files and Nginx configuration from the VPS. Delete dedicated policies/functions only after checking that no other distribution uses them. Preserve the DNS zone and certificates used by other services.

## Rollback

If production verification fails, restore the saved apex/`www` DNS records to the existing CloudFront distribution while the old hosting is still available. Investigate the Vercel deployment before attempting the cutover again.
