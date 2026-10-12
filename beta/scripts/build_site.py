from pathlib import Path
from html import escape, unescape
import hashlib
import json
import os
import re
from functools import lru_cache
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "site.json").read_text())
PARTIALS = ROOT / "templates/partials"
WORK = json.loads((ROOT / "content/work.json").read_text())
RELATED_CASES = json.loads((ROOT / "content/related-cases.json").read_text())
DEVICES = json.loads((ROOT / "content/devices.json").read_text())


@lru_cache(maxsize=None)
def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def asset(path, prefix):
    digest = digest_file(ROOT / path)
    return f"{prefix}{path}?v={digest}"


def head(page, prefix):
    path = page["path"]
    canonical_path = "" if path == "index.html" else path.removesuffix("index.html")
    canonical = MANIFEST["base_url"] + canonical_path
    title = escape(page["title"], quote=True)
    description = escape(page["description"], quote=True)
    styles = ["assets/site.css", *page["styles"]]
    if path in RELATED_CASES:
        styles.append("assets/related-cases.css")
    styles.extend(["assets/devices.css", "assets/theme-washed-blue.css"])
    links = "\n".join(f'<link rel="stylesheet" href="{asset(css, prefix)}">' for css in styles)
    person = {
        "@context": "https://schema.org", "@type": "Person",
        "@id": MANIFEST["base_url"] + "#felipe", "name": "Felipe Amorim",
        "url": MANIFEST["base_url"], "jobTitle": "Senior AI product designer",
        "homeLocation": {"@type": "Place", "name": "Madrid, Spain"},
        "sameAs": ["https://www.linkedin.com/in/felipecaroe/", "https://www.behance.net/felipecaroe"],
    }
    extra = [node for node in page["schema"] if node.get("@type") not in ("Person", "WebPage")]
    nodes = [person, {"@context": "https://schema.org", "@type": "WebPage", "url": canonical,
                      "name": page["title"], "description": page["description"],
                      "author": {"@id": person["@id"]}}, *extra]
    schema = json.dumps(nodes, ensure_ascii=False).replace("<", "\\u003c")
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f7f9fc">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="noindex,follow,noarchive">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="{prefix}img/favicon.ico">
{links}
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{MANIFEST["base_url"]}img/og-portfolio-blue.png">
<meta property="og:image:alt" content="Felipe Amorim. Senior product design. AI expertise. Madrid / Europe.">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{MANIFEST["base_url"]}img/og-portfolio-blue.png">
<meta name="twitter:image:alt" content="Felipe Amorim. Senior product design. AI expertise. Madrid / Europe.">
<script type="application/ld+json">{schema}</script>'''


def partial(name, prefix):
    return (PARTIALS / name).read_text().replace("{{ROOT}}", prefix)


def device_image(image, kind, source):
    if kind not in ("phone", "tablet", "native", "watch", "composition"):
        raise ValueError(f"Unknown device type {kind} for {source}")
    spec = DEVICES[source]
    width, height = spec["size"]
    bounds = spec.get("bounds", [0, 0, width, height])
    left, top, right, bottom = bounds
    box_width, box_height = right - left, bottom - top
    ratio = box_width / box_height
    classes = ["device-mockup", f"device-mockup--{kind}"]
    if kind in ("phone", "tablet"):
        inset = .0185 if kind == "phone" else .0118
        ratio /= 1 - 2 * inset + 2 * inset * ratio
    if spec.get("shadow"):
        classes.append("device-mockup--source-shadow")
    if spec.get("clip"):
        classes.append("device-mockup--clipped")
    geometry = f"--device-ratio:{ratio:.8f}"
    if kind not in ("phone", "tablet"):
        geometry += (
            f";--asset-width:{100 * width / box_width:.6f}%"
            f";--asset-height:{100 * height / box_height:.6f}%"
            f";--asset-left:{-100 * left / box_width:.6f}%"
            f";--asset-top:{-100 * top / box_height:.6f}%"
        )
    if kind in ("phone", "tablet") and spec.get("screen_crop"):
        classes.append("device-mockup--screen-crop")
        geometry += (f";--crop-width:{100 * width / box_width:.6f}%;--crop-height:{100 * height / box_height:.6f}%;--crop-left:{-100 * left / box_width:.6f}%;--crop-top:{-100 * top / box_height:.6f}%")
    attributes = {**image, "class": "device-mockup__image"}
    attributes.pop("data-device", None)
    attributes.setdefault("width", str(width))
    attributes.setdefault("height", str(height))
    attributes.setdefault("decoding", "async")
    visual = '<img ' + ' '.join(f'{key}="{escape(str(value), quote=True)}"' for key, value in attributes.items()) + '>'
    if kind in ("phone", "tablet"):
        visual = f'<span class="device-mockup__body"><span class="device-mockup__screen">{visual}</span></span>'
    return f'<span class="{" ".join(classes)}" style="{geometry}">{visual}</span>'


def template_devices(text, path):
    def render(match):
        attributes = {key: unescape(value) for key, value in re.findall(r'([\w-]+)="([^"]*)"', match[0])}
        kind = attributes.pop("data-device")
        source = ((ROOT / path).parent / attributes["src"]).resolve().relative_to(ROOT).as_posix()
        return device_image(attributes, kind, source)
    return re.sub(r'<img\b[^>]*\bdata-device="[^"]+"[^>]*>', render, text)


def work_cards(prefix, selected=None):
    cards = WORK if selected is None else [card for card in WORK if card["href"] in selected]
    result = []
    arrow = '<svg class="arrow-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M4 12 12 4M5 4h7v7"/></svg>'
    for card in cards:
        image = card["image"]
        visual = device_image({**image, "src": prefix + image["src"]}, card["device"], image["src"])
        tags = ''.join(f'<span>{escape(tag)}</span>' for tag in card["tags"])
        result.append(f'<a class="{card["classes"]}" href="{prefix}{card["href"]}"><div class="work-image work-image--device">{visual}<div class="work-image__tags">{tags}</div></div><div class="work-details"><div><h3>{escape(card["title"])}</h3><p>{escape(card["description"])}</p></div><span class="arrow" aria-hidden="true">{arrow}</span></div></a>')
    return '\n'.join(result)


def related_cases(page, prefix):
    config = RELATED_CASES.get(page["path"])
    if not config:
        return ""
    by_href = {item["href"]: item for item in WORK}
    cards = []
    for related in config["cases"]:
        item = by_href[related["href"]]
        image = item["image"]
        image_src = image["src"]
        target = ROOT / item["href"]
        relative_href = os.path.relpath(target, (ROOT / page["path"]).parent)
        if target.is_dir():
            relative_href += "/"
        thumbnail = device_image({"src": prefix + image_src, "alt": "", "loading": "lazy"}, item["device"], image_src)
        cards.append(
            f'<a class="related-case" href="{escape(relative_href, quote=True)}">'
            f'<span class="related-case__visual">{thumbnail}</span>'
            f'<span class="related-case__copy"><span class="related-case__reason">{escape(related["reason"])}</span>'
            f'<strong>{escape(item["title"])}</strong><span class="related-case__description">{escape(item["description"])}</span>'
            '<span class="related-case__link">Explore case <svg class="arrow-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M4 12 12 4M5 4h7v7"/></svg></span></span></a>'
        )
    return (
        '<section class="related-work" aria-label="Related work"><div class="shell">'
        '<div class="related-work__heading"><div class="section-index">Related work</div>'
        f'<p>{escape(config["description"])}</p></div>'
        f'<div class="related-work__grid">{"".join(cards)}</div></div></section>'
    )


def version_media(text, output_path):
    def version_url(value):
        url = urlsplit(value)
        if url.scheme or url.netloc:
            return value
        target = (output_path.parent / unquote(url.path)).resolve()
        if not target.is_file():
            return value
        query = url.query + "&" if url.query else ""
        return url._replace(query=query + "v=" + digest_file(target)).geturl()

    def tag(match):
        def reference(attribute):
            key, value = attribute[1], attribute[2]
            if key == "srcset" and not value.startswith("data:"):
                candidates = []
                for item in value.split(","):
                    parts = item.strip().split()
                    candidates.append(" ".join([version_url(parts[0]), *parts[1:]]))
                value = ", ".join(candidates)
            else:
                value = version_url(value)
            return f'{key}="{escape(value, quote=True)}"'
        return re.sub(r'(src|srcset|poster)="([^\"]+)"', reference, match[0])
    return re.sub(r'<(?:img|video|source)\b[^>]*>', tag, text)


def defer_background_video(text):
    def defer(match):
        video = match[0].replace(' autoplay', '').replace('preload="auto"', 'preload="none"')
        return re.sub(r'(<source\b[^>]*?)\bsrc=', r'\1data-src=', video)
    return re.sub(r'<video\b[^>]*class="site-background-video"[^>]*>.*?</video>', defer, text)


def build(page):
    path = page["path"]
    relative = os.path.relpath(ROOT, (ROOT / path).parent)
    prefix = "" if relative == "." else relative + "/"
    nav = "".join(
        f'<a href="{prefix}{target}"'
        + (' aria-current="page"' if key == page["section"] else "") + f'>{label}</a>'
        for key, target, label in [("work", "work.html", "Work"), ("services", "services.html", "Services"),
                                   ("leadership", "leadership.html", "About")]
    )
    header = partial("header.html", prefix).replace("{{NAV}}", nav).replace(
        "{{CONTACT_CURRENT}}", ' aria-current="page"' if page["section"] == "contact" else "")
    invitation = "" if page["compact_footer"] else partial("footer-invitation.html", prefix)
    footer = partial("footer.html", prefix).replace("{{FOOTER_INVITATION}}", invitation)
    template = (ROOT / "templates/pages" / path).read_text()
    output = template.replace("{{SITE_HEAD}}", head(page, prefix)).replace("{{SITE_HEADER}}", header)
    output = output.replace("{{SITE_FOOTER}}", footer).replace("{{SITE_SCRIPT}}", f'<script src="{asset("assets/site.js", prefix)}" defer></script>')
    output = output.replace("{{WORK_CARDS}}", work_cards(prefix))
    output = output.replace("{{HOME_CARDS}}", work_cards(prefix, {"work/luzia-new-chat/", "work/atletico-de-madrid.html", "cases/drafts/services-hub/", "work/pizza-hut.html"}))
    related = related_cases(page, prefix)
    if related:
        closing_marker = '<section class="closing">' if path == "work/luzia-new-chat/index.html" else '<section class="case-close section">'
        if closing_marker not in output:
            raise ValueError(f"Missing case CTA insertion point in {path}")
        output = output.replace(closing_marker, related + closing_marker, 1)
    output = template_devices(output, path)
    output = defer_background_video(output)
    output = version_media(output, ROOT / path)
    if "{{" in output:
        raise ValueError(f"Unresolved template field in {path}")
    (ROOT / path).write_text("\n".join(line.rstrip() for line in output.splitlines()) + "\n")


for page in MANIFEST["pages"]:
    build(page)
for name in ("plan", "design"):
    path = ROOT / f"work/luzia-new-chat/{name}.html"
    path.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,follow,noarchive">
<link rel="canonical" href="{MANIFEST["base_url"]}work/luzia-new-chat/">
<meta http-equiv="refresh" content="0; url=./"><title>Luzia · New chat | Felipe Amorim</title>
</head><body><p><a href="./">Open the combined Luzia new-chat case.</a></p></body></html>''')
print(f"Built {len(MANIFEST['pages'])} pages and two case redirects with shared chrome and hashed assets.")
import sys
sys.dont_write_bytecode = True
from audit_site import audit

audit()
