# Marine Consultants Final Consolidated Website

This repository contains the final cleaned website build consolidated from multiple Google Stitch exports. The active site is now a single production-ready static build with one approved version of each core page, consistent navigation and footer structure, deeper product/service routing, and regionally grounded Trinidad & Tobago / Caribbean marine supply and service positioning.

## What this project is

The site is positioned as a regional marine supply and service website for:

- marine supply
- marine safety products
- inspections
- maintenance support
- certification support
- technical procurement
- vessel support
- regional B2B inquiry flow

The current build intentionally avoids unsupported global, multinational, or inflated business claims.

## Final structure

- `index.html`
  - Home
- `about.html`
  - Main about page
- `products.html`
  - Product catalog overview
- `services.html`
  - Services overview
- `resources.html`
  - Catalogue / resources hub
- `news.html`
  - News / updates page
- `contact.html`
  - General contact page
- `request-quote.html`
  - Canonical request-a-quote page
- `about/`
  - `company-overview.html`
  - `quality-compliance.html`
  - `leadership.html`
- `categories/`
  - All active product category pages
- `services/`
  - All active service pages
- `products/`
  - Representative product detail page
- `inquiries/`
  - `product-inquiry.html`
  - `service-inquiry.html`
- `assets/`
  - Shared CSS and JavaScript for the final live site
- `canonical_sources/`
  - The selected Stitch HTML pages kept as the final reference set used during consolidation
- `archive/legacy-exports/`
  - Raw and legacy Stitch exports removed from active use
- `build_static.py`
  - Static generator for the final consolidated site
- `server.py`
  - Lightweight static dev server
- `audit_static.py`
  - Browser-backed verification script

## Canonical pages kept

The final active core pages are:

- Home: `index.html`
- About: `about.html`
- Products: `products.html`
- Services: `services.html`
- Catalogue / Resources: `resources.html`
- News / Updates: `news.html`
- Contact: `contact.html`
- Request a Quote: `request-quote.html`

## What was broken

- The downloaded Stitch passes contained duplicate core-page concepts.
- Different exports used conflicting home, about, product, service, contact, and quote variants.
- Some pages still contained invented or unsupported wording such as global positioning, fake offices, fake dates, fake response claims, and inflated authority language.
- Navigation and footer structures were inconsistent across variants.
- Active routing still reflected old page concepts like `support` and `industries`.
- Several actions looked interactive but had no working behavior.
- Old deploy output and raw exports were mixed together, making it unclear which files were live.

## What was fixed

- Consolidated the project into one active static site build.
- Kept one canonical version of each required core page.
- Added nested product category, service, about, and inquiry pages.
- Standardized the shared header and footer.
- Removed old active `support.html`, `industries.html`, and `quote.html` usage.
- Added Vercel redirects for legacy routes:
  - `/quote.html` -> `/request-quote.html`
  - `/support.html` -> `/services/support-request.html`
  - `/industries.html` -> `/about.html`
- Replaced unsupported or invented marketing claims with grounded regional copy or explicit placeholders.
- Archived raw and legacy Stitch exports out of the active root structure.
- Added shared front-end behavior for:
  - mobile navigation
  - catalog/news filtering
  - form confirmation states
  - placeholder resource actions

## Placeholder content still needing manual business input

The following placeholder content remains intentionally unresolved because it was not verified in the source exports:

- `Company Overview Placeholder`
- `Leadership Placeholder`
- `Contact Details Placeholder`
- `Compliance Information Placeholder`
- `Catalogue Download Placeholder`
- `Product Description Placeholder`
- `Service Description Placeholder`
- approved supplier, stock, and technical specification details
- approved legal copy for privacy and terms pages

## Assumptions and limitations

- The final site preserves the strongest visual direction from the selected Stitch references, but the codebase is now a consolidated static build rather than a runtime wrapper around every raw export.
- No backend or CRM endpoint was present in the Stitch downloads, so forms are implemented as local confirmation flows only.
- Product, service, compliance, and company-detail placeholders should be replaced with verified business information before public launch.
- External images and fonts still load from the original hosted URLs used by Stitch.

## How to run locally

Requirements:

- Python 3.10+ recommended

Start the local server:

```powershell
python server.py
```

Open:

```text
http://127.0.0.1:8000
```

## How to rebuild the site

```powershell
python build_static.py
```

This regenerates:

- all active `.html` routes
- `assets/site.css`
- `assets/site.js`
- `favicon.ico`
- `vercel.json`

## How to verify the site

Run the browser-backed audit:

```powershell
python audit_static.py --timeout 10
```

The audit checks:

- all active routes return `200`
- internal browser-rendered links resolve
- no live `href="#"` links remain
- no unresolved Stitch placeholders remain
- banned fake/global phrases are not present in the live output

## Technical issues not fully resolved automatically

- Real contact details, compliance approvals, supplier documentation, and legal copy were not verifiable from the Stitch exports and remain placeholders by design.
- The representative product detail page keeps the structure of a detail template, but technical values should be inserted only after manual verification.
