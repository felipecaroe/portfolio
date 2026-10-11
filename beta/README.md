# Portfolio source

This is the source for the live portfolio at `https://felipecaroe.github.io/portfolio/`. Local preview pages use `noindex,follow,noarchive`; the release builder emits the public-only site with production canonicals and indexing enabled. GitHub Actions deploys only `.release/public/`, so beta preview routes and working material are excluded.

## Source map

| Source | Edit here for |
| --- | --- |
| `templates/pages/` | Current content and case narratives. Paths mirror output pages. |
| `templates/partials/` | Shared header, footer and footer invitation. |
| `content/work.json` | All 15 covers, images, tags and descriptions. Home and Work share these entries. |
| `content/devices.json` | Original image dimensions, visible shell bounds and existing shadows. |
| `site.json` | Titles, descriptions, navigation section and page-specific styles. |
| `assets/site.css` | Shared layout, components, responsive behaviour and hover motion. |
| `assets/theme-washed-blue.css` | Palette, loaded last on every page. |
| `assets/devices.css` | One proportional device renderer for covers, galleries and related work. Native shells stay native; raw screens receive a thin shell. |
| `cases/drafts/*/case.css` | Case-specific layout. |
| `assets/case-compositions.css` | Ipiranga, Raiô and SkateKing compositions. |
| `assets/site.js` | Contact email drafts and capability carousel. |
| `reviews/` | Current publication review; earlier evidence is archived outside the website. |

## Build

From `website/`:

```sh
python3 beta/scripts/build_site.py
python3 beta/scripts/audit_site.py
```

The builder renders 24 current pages and two old Luzia URLs redirecting to the combined case. The release allowlist publishes 22 public pages. CSS, JavaScript and media versions come from file contents. The audit checks local links and assets, shared chrome, stylesheet order, metadata, device geometry and template coverage.

Edit templates and content first, then build. Direct edits to generated HTML will be replaced. The obsolete generators were backed up in the workspace's `archive/migration-notes/`; do not use them to rebuild.

## Preview

```sh
python3 -m http.server 8766 --directory /Users/caroe/Documents/Codex/projects/freelance/website
```

Open `http://localhost:8766/beta/`. Original case material stays in `../../cases/`. Copy only selected, cleared assets into beta. Preserve each screen's proportions rather than stretching it to fit a fixed shell.

Mark an unframed screen in a template with `data-device="phone"` or `data-device="tablet"`. Use `data-device="native"` for an image that already has a shell. Add its actual dimensions to `content/devices.json`; transparent native assets also need the visible phone bounds so shadows and export padding cannot change alignment. Do not apply image transforms on hover: move the device wrapper as a whole.

## Archived working material

Earlier review snapshots and unused Espanyol source notes moved to `../archive/2026-10-10/` relative to the website repository root, outside the served beta. See `website-moves.json` there for exact paths. Current case media, source kit images referenced by pages and production assets remain in place. The existing `cases/source-kits/` contains live image dependencies, so do not remove it without migrating those references.
