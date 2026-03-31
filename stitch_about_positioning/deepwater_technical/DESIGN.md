```markdown
# Design System Specification: Marine Industrial Excellence

## 1. Overview & Creative North Star: "The Nautical Blueprint"

This design system is built to reflect the precision of marine engineering and the vastness of the maritime industry. Our Creative North Star is **"The Nautical Blueprint."** 

We move beyond the "standard corporate portal" by treating the UI as a technical instrument. The aesthetic is defined by high-contrast legibility, rigorous structural logic, and an editorial layout style that favors intentional white space over cluttered dividers. We break the "template" look by utilizing asymmetrical content blocks and overlapping "Technical Insets" that mimic the layering of blueprints and navigational charts.

The goal is to project absolute operational reliability. Every pixel must feel calculated, every margin intentional, and every transition purposeful.

---

## 2. Colors & Surface Logic

The palette is rooted in the depth of the ocean (`primary: #001628`) and the clarity of technical documentation (`surface: #f4faff`).

### The "No-Line" Rule
To achieve a high-end, bespoke feel, **1px solid borders are strictly prohibited** for sectioning or containment. Boundaries are defined exclusively through background tonal shifts. Use `surface_container_low` for secondary sections and `surface_container_highest` for interactive sidebars. This creates a sophisticated, "carved" look rather than a "boxed" one.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. Use the following tiers to define depth without shadows:
*   **Base:** `surface` (#f4faff) - The canvas.
*   **Level 1 (Subtle Inset):** `surface_container_low` (#e9f6fd) - Large content areas.
*   **Level 2 (Active Component):** `surface_container` (#e3f0f8) - Cards and navigation rails.
*   **Level 3 (Focus):** `surface_container_high` (#ddeaf2) - Popovers and search bars.

### The "Glass & Technical Gradient" Rule
For hero sections or primary calls to action, use a "Technical Gradient" transitioning from `primary` (#001628) to `primary_container` (#002b47) at a 135-degree angle. This adds "visual soul" without looking like a consumer-grade template. For floating navigation elements, use **Glassmorphism**: `surface_container_lowest` at 80% opacity with a `24px` backdrop-blur to allow the maritime blues to bleed through.

---

## 3. Typography: Technical Authority

We pair **Manrope** (Display/Headline) for a modern, industrial feel with **Inter** (Body/Label) for peak legibility in data-heavy environments.

*   **Display (LG/MD/SM):** Use Manrope with a `-0.02em` letter spacing. These are your "billboard" moments. Use `primary` for maximum authority.
*   **Headlines & Titles:** Manrope. Use `on_surface` (#111d23). Headlines should be set with generous top margins (`spacing-16`) to create an editorial, airy feel.
*   **Body (LG/MD/SM):** Inter. Use `on_surface_variant` (#42474d) for long-form text to reduce eye strain.
*   **Labels:** Inter (Bold). Use for technical data points and metadata. Labels should often be uppercase with `0.05em` tracking to mimic industrial stamping.

---

## 4. Elevation & Depth: Tonal Layering

Traditional drop shadows are too "software-generic." We use **Tonal Layering** to communicate elevation.

*   **The Layering Principle:** To lift a card, place a `surface_container_lowest` (#ffffff) element on top of a `surface_container_low` (#e9f6fd) background. The contrast provides the "lift."
*   **Ambient Shadows:** If a floating state is required (e.g., a Modal), use a diffused shadow: `box-shadow: 0 20px 40px rgba(17, 29, 35, 0.06)`. The color is a tint of `on_surface`, never pure black.
*   **The "Ghost Border" Fallback:** For high-density data tables where separation is critical, use `outline_variant` (#c3c7ce) at **15% opacity**. It should be felt, not seen.

---

## 5. Components & Primitive Styles

### Buttons
*   **Primary:** `tertiary_container` (#481c00) background with `on_tertiary_container` (#eb6a00) text. This "Safety Orange" provides high-contrast visibility against maritime blues. Shape: `md` (0.375rem).
*   **Secondary:** `primary` (#001628) with `on_primary` (#ffffff).
*   **Tertiary:** Ghost style. No background, Manrope Bold, `0.5rem` horizontal padding.

### Cards & Data Lists
*   **Constraint:** Zero dividers. Use `spacing-8` or `spacing-10` vertical gaps.
*   **Style:** Cards use `surface_container_lowest`. On hover, shift the background to `surface_bright` and apply the Ambient Shadow.

### Input Fields
*   **Visuals:** Inset style using `surface_container_low`. No borders. A `2px` bottom stroke in `primary` appears only on `:focus`.
*   **Typography:** Labels use `label-sm` in `outline`.

### Specialized Component: The Technical Header
In hero sections, use an asymmetrical layout. The Headline (Display-LG) sits on the left, while a "Technical Inset" (a small `surface_container_high` box containing metadata or coordinates) sits offset to the right, breaking the standard grid.

---

## 6. Do’s and Don’ts

### Do:
*   **Use Asymmetry:** Balance a heavy image on the right with a high-contrast `display-lg` headline on the left, offset by `spacing-12`.
*   **Respect the Grid:** Use the `spacing-4` (1rem) as your base unit for all alignments.
*   **Embrace "Technical teal":** Use `secondary` (#48626e) for iconography to maintain a "slate" industrial vibe.

### Don’t:
*   **Don't use 100% Black:** Always use `primary` or `on_surface` for dark tones to keep the "Maritime" DNA.
*   **Don't use Rounded Corners > 0.75rem:** Marine engineering is about structural integrity; overly rounded "bubble" UI (full-radius) feels too playful and diminishes trust.
*   **Don't use Center-Alignment for Long Text:** Technical layouts should be left-aligned to mimic schematics and reports.

---

## 7. Signature Interaction Pattern: The "Blue-Shift"
When a user interacts with a container, avoid "glow" effects. Instead, use a subtle "Blue-Shift": the background color transitions from `surface_container` to `primary_container` over 200ms, creating a deep, immersive focus state that signals technical precision.```