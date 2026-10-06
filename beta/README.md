# Portfolio beta

The active site under review uses the washed-blue palette, shared navigation and coral actions. Pages carry `noindex,follow,noarchive`. Production files at the repository root are separate.

## Source map

| Source | Edit here for |
| --- | --- |
| `templates/pages/` | Current content and case narratives. Paths mirror output pages. |
| `templates/partials/` | Shared header, footer and footer invitation. |
| `content/work.json` | All 14 covers, images, tags and descriptions. Home and Work share these entries. |
| `site.json` | Titles, descriptions, navigation section and page-specific styles. |
| `assets/site.css` | Shared layout, components, responsive behaviour and hover motion. |
| `assets/theme-washed-blue.css` | Palette, loaded last on every page. |
| `cases/drafts/phone-shell.css` | Shared phone geometry fitted to each source screen. |
| `cases/drafts/*/case.css` | Case-specific layout. |
| `assets/case-compositions.css` | Ipiranga, Raiô and SkateKing compositions. |
| `assets/site.js` | Contact email drafts and capability carousel. |
| `reviews/` | Dated review evidence. |

## Build

From `website/`:

```sh
python3 beta/scripts/build_site.py
python3 beta/scripts/audit_site.py
```

The builder renders 23 current pages and two old Luzia URLs redirecting to the combined case. CSS, JavaScript and media versions come from file contents. The audit checks local links and assets, shared chrome, stylesheet order, metadata and template coverage.

Edit templates and content first, then build. Direct edits to generated HTML will be replaced. The obsolete generators were backed up in the workspace's `archive/migration-notes/`; do not use them to rebuild.

## Preview

```sh
python3 -m http.server 8766 --directory /Users/caroe/Documents/Codex/projects/freelance/website
```

Open `http://localhost:8766/beta/`. Original case material stays in `../../cases/`. Copy only selected, cleared assets into beta. Preserve each screen's proportions rather than stretching it to fit a fixed shell.
