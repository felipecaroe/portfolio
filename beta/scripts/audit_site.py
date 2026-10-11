from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "site.json").read_text())
DEVICES = json.loads((ROOT / "content/devices.json").read_text())
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = set()
        self.errors = []
        self.stack = []
        self.devices = 0
        self.device_images = 0
        self.drawer_cover_images = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = attributes.get("class", "").split()
        if "device-mockup" in classes:
            self.devices += 1
            ratio = re.search(r"--device-ratio:([\d.]+)", attributes.get("style", ""))
            if not ratio or not math.isfinite(float(ratio[1])) or float(ratio[1]) <= 0:
                self.errors.append("Device has missing or invalid proportions")
        if tag == "img" and "device-mockup__image" in classes:
            self.device_images += 1
        if tag == "img" and "rcde-demo__home" in classes:
            self.drawer_cover_images += 1
        if "data-device" in attributes:
            self.errors.append("Unrendered device image")
        if tag not in VOID:
            self.stack.append(tag)
        if "id" in attributes:
            if attributes["id"] in self.ids:
                self.errors.append(f"Duplicate id: {attributes['id']}")
            self.ids.add(attributes["id"])
        for key in ("src", "data-src", "href", "poster"):
            if attributes.get(key):
                self.references.append(attributes[key])
        if attributes.get("srcset"):
            self.references.extend(item.strip().split()[0] for item in attributes["srcset"].split(","))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"Unbalanced closing tag: {tag}")


def audit():
    errors = []
    for source, device in DEVICES.items():
        width, height = device["size"]
        left, top, right, bottom = device.get("bounds", [0, 0, width, height])
        if not (0 <= left < right <= width and 0 <= top < bottom <= height):
            errors.append(f"{source}: Invalid visible device bounds")
        if not (ROOT / source).is_file():
            errors.append(f"{source}: Missing device source")
    pages = {entry["path"] for entry in MANIFEST["pages"]}
    templates = {path.relative_to(ROOT / "templates/pages").as_posix() for path in (ROOT / "templates/pages").rglob("*.html")}
    if pages != templates:
        errors.append("Page manifest and templates differ")
    parsed = {}
    for path in sorted(pages):
        page = Page()
        text = (ROOT / path).read_text()
        page.feed(text)
        parsed[(ROOT / path).resolve()] = page
        errors.extend(f"{path}: {issue}" for issue in page.errors)
        if page.stack:
            errors.append(f"{path}: Unclosed tags: {page.stack}")
        if page.devices != page.device_images + page.drawer_cover_images:
            errors.append(f"{path}: Device wrappers and images differ")
        css = re.findall(r'<link rel="stylesheet" href="([^\"]+)"', text)
        if not css or "assets/site.css?v=" not in css[0] or "assets/theme-washed-blue.css?v=" not in css[-1]:
            errors.append(f"{path}: Shared styles missing or in the wrong order")
        if len(css) < 3 or "assets/devices.css?v=" not in css[-2]:
            errors.append(f"{path}: Shared device renderer missing or in the wrong order")
        for required in ('<meta name="robots" content="noindex', '<link rel="canonical"', '<meta name="description"', 'class="site-header"', 'class="site-footer"', 'id="main"'):
            if required not in text:
                errors.append(f"{path}: Missing {required}")
        if len(re.findall(r'<h1\b', text)) != 1:
            errors.append(f"{path}: Expected one h1")
        if "{{" in text:
            errors.append(f"{path}: Unresolved template field")
    for source, page in parsed.items():
        for reference in page.references:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            target = (source.parent / unquote(url.path)).resolve() if url.path else source
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                errors.append(f"{source.relative_to(ROOT)}: Missing local target {reference}")
            elif url.fragment and target in parsed and unquote(url.fragment) not in parsed[target].ids:
                errors.append(f"{source.relative_to(ROOT)}: Missing fragment {reference}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Passed: {len(pages)} pages, shared styles and devices, chrome, metadata, balanced markup and local references.")


if __name__ == "__main__":
    audit()
