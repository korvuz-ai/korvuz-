"""Generate the English static portfolio. Requires only Python's standard library."""
from html import escape
import hashlib
import json
from pathlib import Path
from string import Template
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PDF = "/Nuntawat_Fangritlong_Senior_DevOps_Specialist.pdf"


def icon(name):
    return f'<svg aria-hidden="true"><use href="#i-{escape(name)}"></use></svg>'


def detail_body(item):
    body = "".join(f"<p>{escape(p)}</p>" for p in item["paragraphs"])
    body += "<ul>" + "".join(f"<li>{escape(p)}</li>" for p in item["bullets"]) + "</ul>"
    if item.get("closing"):
        body += f'<p>{escape(item["closing"])}</p>'
    if item.get("url"):
        body += f'<p><a class="textlink" href="{escape(item["url"])}" target="_blank" rel="noopener">Open {escape(item["title"])}</a></p>'
    return body


def document(title, description, route, body):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Nuntawat Fangritlong</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="theme-color" content="#161622"><link rel="canonical" href="https://korvuz.site{route}">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:type" content="article"><meta property="og:url" content="https://korvuz.site{route}"><meta property="og:image" content="https://korvuz.site/og-image.png">
<link rel="icon" href="/assets/icons/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/css/reference.css"><link rel="stylesheet" href="/assets/css/portfolio.css"></head>
<body class="detail-document"><a class="skip-link" href="#content">Skip to content</a><header class="detail-header"><nav class="wrap" aria-label="Main navigation"><a class="brand" href="/"><span class="brand-icon">N</span>Nuntawat.</a><a href="/#work">Back to portfolio</a></nav></header><main class="detail-page wrap" id="content">{body}</main><footer class="detail-footer wrap"><p>Nuntawat Fangritlong. Senior DevOps Specialist.</p><a href="mailto:nuntawat.works@gmail.com">Get in touch</a></footer></body></html>'''


def build():
    content = json.loads((ROOT / "site/content.json").read_text())
    details = {}
    career_rows = []
    for job in content["jobs"]:
        career_rows.append(f'''<article class="exp-card reveal"><p class="exp-year">{escape(job["date"])}</p><div><h3>{escape(job["title"])}</h3><p class="company">{escape(job["company"])}</p><ul class="exp-list">{"".join("<li>"+escape(b)+"</li>" for b in job["bullets"])}</ul></div></article>''')
    skill_rows = "\n".join(f'<div class="skill-row"><h3>{escape(k)}</h3><p>{escape(v)}</p></div>' for k, v in content["skills"])
    cases, products, notes = [], [], []
    for group, prefix in [("cases", "work"), ("products", "projects"), ("notes", "notes")]:
        for item in content[group]:
            route = f'/{prefix}/{item["slug"]}/'
            item["route"] = route
            details[item["id"]] = item
            path = PUBLIC / route.strip("/") / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            body = f'<h1>{escape(item["title"])}</h1><p class="detail-intro">{escape(item["summary"])}</p>{detail_body(item)}<p class="detail-tags">{escape(item["tags"])}</p>'
            path.write_text(document(item["title"], item["summary"], route, body) + "\n")
            link = f'<a class="mini-link" href="{route}" data-modal="{item["id"]}">Read more</a>'
            if group == "cases":
                cases.append(f'''<article class="case-card reveal"><div class="case-art {item["art"]}" aria-hidden="true"><div class="case-symbol">{icon(item["icon"])}</div><span class="case-art-title">{escape(item["label"])}</span></div><div class="case-copy"><h3>{escape(item["title"])}</h3><p>{escape(item["summary"])}</p><div class="case-foot"><span class="tech-tags">{escape(item["tags"])}</span>{link}</div></div></article>''')
            elif group == "products":
                illustrated = item["image"].endswith(".svg")
                alt = f'Illustrated {item["title"]} interface' if illustrated else 'Korvuz Atlas public landing page'
                products.append(f'''<article class="product-card reveal"><div class="product-picture"><img src="/assets/portfolio/{escape(item["image"])}" alt="{escape(alt)}" width="800" height="460" loading="lazy"></div><div class="product-body"><p class="product-category">{escape(item["category"])}</p><h3>{escape(item["title"])}</h3><p>{escape(item["summary"])}</p><div class="product-footer"><span class="tags">{escape(item["tags"])}</span>{link}</div></div></article>''')
            else:
                notes.append(f'''<article class="article-card reveal"><div class="article-icon" aria-hidden="true">{icon(item["icon"])}</div><h3>{escape(item["title"])}</h3><p>{escape(item["summary"])}</p><a class="mini-link" href="{route}" data-modal="{item["id"]}">Read the note</a></article>''')
    schema = {"@context": "https://schema.org", "@type": "Person", "name": content["name"], "jobTitle": content["title"], "url": "https://korvuz.site/", "sameAs": ["https://github.com/korvuz-ai", "https://linkedin.com/in/nuntawat-zeo"]}
    safe_json = lambda value: json.dumps(value, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    template = Template((ROOT / "site/index.template.html").read_text())
    result = template.substitute(PDF=PDF, ICONS=(ROOT / "site/icons.svg").read_text(), PERSON_SCHEMA=safe_json(schema), DETAIL_DATA=safe_json(details), CAREER_ROWS="\n".join(career_rows), SKILL_ROWS=skill_rows, CASE_CARDS="\n".join(cases), PRODUCT_CARDS="\n".join(products), NOTE_CARDS="\n".join(notes))
    (PUBLIC / "index.html").write_text(result)
    body = '<h1>Engineering notes</h1><p class="detail-intro">Practical thinking about releases, infrastructure automation and Linux operations.</p><div class="notes-index">'
    for item in content["notes"]:
        body += f'<article><h2><a href="{item["route"]}">{escape(item["title"])}</a></h2><p>{escape(item["summary"])}</p></article>'
    body += '</div>'
    (PUBLIC / "notes").mkdir(exist_ok=True)
    (PUBLIC / "notes/index.html").write_text(document("Engineering notes", "Notes on release readiness, repeatable infrastructure and Linux security.", "/notes/", body) + "\n")
    error = document("Page not found", "The page you requested could not be found.", "/404.html", '<h1>Page not found.</h1><p class="detail-intro">This page may have moved. You can return to the portfolio or download the resume.</p><p><a class="btn btn-primary" href="/">Back to portfolio</a></p>')
    error = error.replace('<meta name="theme-color"', '<meta name="robots" content="noindex, follow"><meta name="theme-color"', 1)
    (PUBLIC / "404.html").write_text(error + "\n")
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    sitemap = ET.Element(f"{{{ns}}}urlset")
    for route in ["/", "/notes/"] + [item["route"] for item in details.values()]:
        entry = ET.SubElement(sitemap, f"{{{ns}}}url")
        ET.SubElement(entry, f"{{{ns}}}loc").text = "https://korvuz.site" + route
    ET.indent(sitemap, space="  ")
    ET.ElementTree(sitemap).write(PUBLIC / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    (PUBLIC / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://korvuz.site/sitemap.xml\n")
    manifest = {str(p.relative_to(PUBLIC)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PUBLIC.rglob("*")) if p.is_file()}
    (ROOT / "docs/production-snapshot.sha256.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built English portfolio, {len(details)} detail pages, notes index and 404; {len(manifest)} public files.")


if __name__ == "__main__":
    build()
