from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "site.json").read_text())
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = set()
        self.errors = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if "id" in attributes:
            if attributes["id"] in self.ids:
                self.errors.append(f"Duplicate id: {attributes['id']}")
            self.ids.add(attributes["id"])
        for key in ("src", "href", "poster"):
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
        css = re.findall(r'<link rel="stylesheet" href="([^\"]+)"', text)
        if not css or "assets/site.css?v=" not in css[0] or "assets/theme-washed-blue.css?v=" not in css[-1]:
            errors.append(f"{path}: Shared styles missing or in the wrong order")
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
    print(f"Passed: {len(pages)} pages, shared stylesheet order, chrome, metadata, balanced markup and local references.")


if __name__ == "__main__":
    audit()
