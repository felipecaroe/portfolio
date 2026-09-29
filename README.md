# Felipe Amorim portfolio

Static portfolio and freelance services for Felipe Amorim. GitHub Pages serves the root of `main` at `https://felipecaroe.github.io/portfolio/`.

## Edit and preview

The new site's content and metadata live in `scripts/build_site.py`. The detailed legacy résumé remains in `resume.html`. The shared design is in `assets/site.css`; `assets/site.js` prepares a client email draft from the contact form. Existing imagery remains in `img/`.

Run `python3 scripts/build_site.py` after changing the new site's copy or page structure. This regenerates nine HTML pages and `sitemap.xml` without third-party build dependencies, while preserving the detailed résumé.

Preview from this repository's parent directory:

```sh
python3 -m http.server 8765 --directory ..
```

Then open `http://localhost:8765/portfolio/` if this checkout is named `portfolio`, or use its actual folder name. Navigation works without JavaScript. The contact page uses JavaScript to open a prefilled email draft, and keeps a direct email link for other cases.

## Before publishing

Review public prices, availability, employment dates and case-study claims. The old homepage and résumé disagreed on several outcomes, so this version does not repeat those figures. The existing `cases/impulse.html` URL remains in the repository.

Check the generated HTML and assets at mobile and desktop widths, then review the branch against the actual GitHub Pages base branch. Merging to `main` publishes the site.
