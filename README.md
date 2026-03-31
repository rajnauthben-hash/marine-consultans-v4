# Marine Consultants Stitch Export

This project preserves the downloaded Google Stitch export for the Marine Consultants website and runs it locally with only the minimum practical fixes needed to make the site usable as a multi-page static website.

## Project structure

- `stitch_about_positioning/`
  - Original downloaded Stitch export.
  - Each page remains in its original folder with the original `code.html` and `screen.png`.
- `server.py`
  - Lightweight Python server that serves the original exported HTML files as the source of truth.
  - Applies minimal runtime fixes for routing, missing fallback pages, and client-side interactions.
- `README.md`
  - Project notes, setup steps, and documented fixes.

## Pages served

- `/index.html` -> `home_marine_consultants_limited_full_site_update/code.html`
- `/about.html` -> `about_positioning_verified_content/code.html`
- `/products.html` -> `product_catalog_verified_inventory/code.html`
- `/services.html` -> `services_capabilities/code.html`
- `/support.html` -> `service_coverage_operational_reach/code.html`
- `/industries.html` -> `industries_we_support/code.html`
- `/news.html` -> `news_updates/code.html`
- `/contact.html` -> `contact_regional_reach/code.html`
- `/quote.html` -> `request_a_quote/code.html`
- `/privacy.html` and `/terms.html`
  - Minimal fallback pages added because the export linked to legal pages that were not included in the downloaded Stitch files.

## What was broken

- The export was not a runnable site scaffold. It was a collection of standalone HTML page exports.
- Internal navigation used unresolved Stitch placeholders such as `{{DATA:SCREEN:SCREEN_9}}`.
- Many top-nav, footer, and CTA links were still `#`.
- The export included forms and filter/search UI without working behavior.
- Some pages were missing `<title>` tags or had generic titles.
- The downloaded package did not include privacy or terms pages even though several pages linked to them.
- Mobile header spacing needed a small responsive adjustment to avoid crowding on narrow screens.

## What was fixed

- Built a small Python server that preserves the exported HTML and serves it as a coherent website.
- Mapped Stitch screen placeholders to real routes.
- Added runtime link wiring for unresolved nav/footer/CTA links while preserving the existing page markup.
- Added lightweight client-side behavior for:
  - quote and contact form confirmation states
  - newsletter/demo form confirmation states
  - product catalog search and filter controls
  - contact/support CTA scrolling and related interaction fixes
- Added consistent page titles for all served routes.
- Added minimal fallback `privacy` and `terms` pages because those pages were not included in the export.
- Added small responsive header adjustments for very narrow screens.

## Assumptions and limitations

- The original Stitch HTML files inside `stitch_about_positioning/` were treated as the source of truth and were not redesigned.
- Since no backend was included in the export, form submissions are handled as client-side demo confirmations only.
- Since article detail pages and legal pages were not included in the export, related CTAs were routed to the closest available page/section or to lightweight fallback pages.
- External images and fonts still load from the original remote URLs used by Stitch.

## How to run locally

Requirements:

- Python 3.14+ (or a recent Python 3 version)

Run:

```powershell
python server.py
```

Then open:

```text
http://127.0.0.1:8000
```

To use a different port:

```powershell
python server.py --port 8010
```

## Verification performed

- Confirmed the server wrapper compiles successfully with `python -m py_compile server.py`.
- Confirmed all primary routes return `200` when served locally.
- Verified Stitch placeholder routes are resolved in served output.
- Generated headless Chrome screenshots for the home page at desktop and mobile sizes to validate layout.
- Confirmed there were no blocking runtime failures while rendering the site locally.

## GitHub readiness

- The project is ready to be committed and pushed once a GitHub remote is available.
- In this environment, `git.exe` is available directly, but GitHub CLI/repo creation tooling was not available on PATH.
- A remote repository URL was not provided in the original request, so remote push setup may still require one final step.
