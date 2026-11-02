# Portfolio checks and PDF sources

The website remains plain HTML, CSS and JavaScript. These optional development tools do not run on GitHub Pages.

- `python3 tools/check_site.py`: dependency-free structural, link, asset and owner-constraint checks. Includes the protected UAS blob, aircraft deletion, CV structure and overview word counts.
- `python3 tools/check_browser.py http://127.0.0.1:8000`: Chromium layout and keyboard checks at 320, 375, 390, 768 and 1440 px. Start a static server from the repository root first (`python3 -m http.server 8000`). Screenshots default to `/tmp/portfolio-browser-check`; change with `--output`.
- `python3 tools/measure_performance.py http://127.0.0.1:8000 /tmp/portfolio-performance.json --overview`: cold/warm CDP lab measurements, including both overviews. Use the same machine, origin/server behaviour and settings for comparisons. `--live` labels a run against the live site; it does not deploy anything. Each navigation is observed for ten seconds after DOMContentLoaded without scrolling. Media networking may not obey the same CDP throttle as document resources, so these figures are lab observations, not a guaranteed mobile connection or field percentiles. Report incomplete transfers and do not equate text LCP with all images finishing.
- `python3 tools/build_cvs.py`: regenerate both PDFs from `tools/cv-content.json`. Review the content, extracted PDF text, rendered pages, page breaks and links before committing replacements. Current outputs: two-page engineering CV at the existing resume URL and two-page procurement CV.

The browser, performance and PDF tools require Python Playwright and Chromium in a development environment (`pip install playwright`, then `python -m playwright install chromium`). They add no dependency to the published site. PDF text/render checks used Poppler's `pdftotext`, `pdfinfo` and `pdftoppm`.

No routine check merges, pushes or deploys the site. Keep original handovers and local screenshots/measurement JSON in the Git-ignored `.codex-handover/` directory or `/tmp`.

- `python3 tools/check_cvs.py`: uses Poppler to check both generated CVs against their canonical JSON text, expected two-page A4 layout, tagged output, approved contact and clickable URL targets. Render and visually inspect each page as well.
