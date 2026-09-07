---
name: Clinical Clarity
colors:
  surface: '#f9f9ff'
  surface-dim: '#cfdaf2'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eeff'
  surface-container-high: '#dee8ff'
  surface-container-highest: '#d8e3fb'
  on-surface: '#111c2d'
  on-surface-variant: '#3d4947'
  inverse-surface: '#263143'
  inverse-on-surface: '#ecf1ff'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#006b5f'
  on-secondary: '#ffffff'
  secondary-container: '#6df5e1'
  on-secondary-container: '#006f64'
  tertiary: '#b90538'
  on-tertiary: '#ffffff'
  tertiary-container: '#dc2c4f'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#71f8e4'
  secondary-fixed-dim: '#4fdbc8'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005048'
  tertiary-fixed: '#ffdadb'
  tertiary-fixed-dim: '#ffb2b7'
  on-tertiary-fixed: '#40000d'
  on-tertiary-fixed-variant: '#92002a'
  background: '#f9f9ff'
  on-background: '#111c2d'
  surface-variant: '#d8e3fb'
typography:
  display:
    fontFamily: Inter
    fontSize: 3.5rem
    fontWeight: '600'
    lineHeight: '1.15'
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Inter
    fontSize: 2.25rem
    fontWeight: '600'
    lineHeight: '1.25'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 1.75rem
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: '1.35'
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: -0.01em
  title-lg:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: '500'
    lineHeight: '1.45'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  body-sm:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0.005em
  label-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '500'
    lineHeight: '1.3'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.025em
  numerical-metric:
    fontFamily: Inter
    fontSize: 2rem
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  space-2xs: 0.25rem
  space-xs: 0.5rem
  space-sm: 0.75rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
  space-3xl: 4rem
  gutter-mobile: 1rem
  gutter-desktop: 1.5rem
  container-max: 80rem
---

## Brand & Style

This design system delivers a clinical-grade, modern healthcare experience rooted in calm assurance, sterile precision, and human-centered warmth. It fuses the systematic rigor of next-generation Material principles with a soft, restorative medical aesthetic. 

The visual environment prioritizes cognitive relief for both clinicians managing high-density diagnostics and patients navigating critical health records. Visual clutter is methodically removed in favor of expansive, breathable surfaces, high-legibility typographic hierarchies, and unambiguous functional color cues. The interface evokes trust, safety, and modern precision—avoiding both the stark, intimidating chill of traditional clinical software and the overly whimsical informality of consumer wellness apps.

## Colors

The palette establishes an immediate sense of hygiene, trust, and clinical efficacy while exceeding WCAG AAA standards for critical typography and WCAG AA standards for interactive controls.

- **Primary (`#0D9488` / `#0F766E`):** Medical Teal anchors core actions, selected states, and authoritative visual anchors. It denotes competence, security, and precision. Deep Teal (`#0F766E`) serves as the hover and active pressed state.
- **Secondary (`#14B8A6` / `#CCFBF1`):** Soothing Mint provides refreshing micro-highlights, progress indicators, active chips, and soft status containers. Mint Wash (`#CCFBF1`) is specifically reserved for low-stress surface fills and positive badge backdrops.
- **Tertiary (`#F43F5E` / `#FB7185`):** Gentle Coral is deployed strictly for clinical alerts, abnormal vital readings, triage counters, and high-urgency notifications. It commands immediate visual triage without inducing panic.
- **Neutral & Surfaces (`#1E293B`, `#64748B`, `#E2E8F0`, `#F8FAFC`, `#FFFFFF`):** High-contrast Slate 800 (`#1E293B`) guarantees crisp, fatigue-free reading across all diagnostic metrics. Pure White (`#FFFFFF`) serves as elevated surface cards, grounded against a baseline canvas of Slate 50 (`#F8FAFC`). Soft border dividers utilize Slate 200 (`#E2E8F0`).

## Typography

Inter serves as the single typographic foundation across all roles, selected for its tall x-height, open apertures, and specialized tabular figure capability.

- Enable `tnum` (tabular numbers) and `cv05` (lower-case l with tail) OpenType features across all quantitative interfaces to prevent visual jitter in live vitals, dosages, and temporal medical records.
- Reserve tight tracking (`-0.02em` to `-0.025em`) exclusively for headers to keep diagnostic titles structured and compact.
- Label styles utilize medium and semibold weights (`500` / `600`) with generous letter-spacing to ensure unambiguous legibility at small sizes on clinical displays and handheld tablets.

## Layout & Spacing

The layout is built upon an 8-point geometric scale, complemented by a 4-point sub-grid for compact data density (vitals displays, badge indicators, and table rows).

- **Grid Architecture:** Desktop displays leverage a 12-column responsive layout with `1.5rem` gutters and max container constraint of `80rem` (`1280px`) to prevent excessively long line lengths in clinical charts. Tablets collapse to an 8-column layout, and mobile views employ a 4-column layout with `1rem` margins.
- **Section Rhythm:** Group related diagnostic information using internal component padding of `space-md` (`1rem`) to `space-lg` (`1.5rem`). Separate modular clinical cards using `space-lg` (`1.5rem`) to maintain clear cognitive segmentation.
- **Density Adaptation:** High-density clinician views (e.g., patient monitoring lists, surgical schedules) compress standard component padding down one tier (e.g., `space-md` down to `space-sm`) while preserving line-height to maintain accessibility.

## Elevation & Depth

Depth is established primarily through crisp tonal layering paired with soft, hyper-diffused ambient teal-tinted shadows, intentionally avoiding heavy dropshadows to preserve a clean, sterile plane.

- **Level 0 (Canvas Base):** Ground layer (`#F8FAFC`). No elevation or border.
- **Level 1 (Clinical Cards & Panels):** White surface (`#FFFFFF`) with a 1px border of Slate 200 (`#E2E8F0`) reinforced by an ambient shadow: `0 1px 3px 0 rgba(15, 23, 42, 0.03), 0 4px 12px 0 rgba(13, 148, 136, 0.02)`.
- **Level 2 (Interactive Floating & Hover States):** Lifted panels, active hover cards, and dropdown panels. Subtle elevated shadow: `0 4px 6px -1px rgba(15, 23, 42, 0.05), 0 10px 24px -3px rgba(13, 148, 136, 0.06)`.
- **Level 3 (Modals & Urgent Diagnostic Overlays):** Highest z-index alerts and prescription confirmation dialogs. `0 20px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.03)`, accompanied by a soothing, desaturated backdrop blur (`backdrop-blur-sm` over `rgba(15, 23, 42, 0.35)`).

## Shapes

The shape system employs roundedness level 2 to project an empathetic, protective, and modern environment without becoming toy-like.

- **Default Components (Inputs, Buttons, Dropdowns):** `0.5rem` (`8px`) to `0.75rem` (`12px`) for precise tactile boundaries that feel modern and balanced.
- **Cards & Data Modules:** `0.75rem` (`12px`) to `1rem` (`16px`) corner radiuses create calm, approachable enclosures for complex laboratory tables and vital charts.
- **Pills & Status Indicators:** Fully rounded (`9999px`) for triage badges, confidence tags, and status chips, visually distinct from actionable rectangular components.

## Components

### Buttons
- **Primary Button:** Deep Medical Teal fill (`#0D9488`), White text (`#FFFFFF`), `0.75rem` (`12px`) border-radius, `0.625rem 1.25rem` padding. Subtle teal shadow on resting state; transitions to `#0F766E` on hover.
- **Secondary Button:** Surface White (`#FFFFFF`), border 1px solid Slate 200 (`#E2E8F0`), text Slate 800 (`#1E293B`). Teal tint hover overlay (`#F0FDFA`).
- **Tertiary / Alert Action:** Coral Fill (`#F43F5E`), White text (`#FFFFFF`), for irreversible clinical actions (e.g., cancelling medication, critical status escalation).

### Chips & Confidence Badges
- Built as full pill shapes (`rounded-full`) using micro typography (`label-sm`).
- **Normal / Healthy Status:** Mint Wash background (`#CCFBF1`), Dark Teal text (`#0F766E`).
- **Diagnostic Alert / High Priority:** Gentle Coral Wash (`#FFE4E6`), Deep Coral text (`#BE123C`).
- **Neutral Reference:** Slate 100 background (`#F1F5F9`), Slate 700 text (`#334155`).

### Input Fields
- Resting: Background `#FFFFFF`, 1px border `#CBD5E1`, text `#1E293B`, `0.625rem 0.875rem` padding, `0.75rem` (`12px`) corner radius.
- Focus: 1px border `#0D9488` accompanied by a soft `3px` focus ring of Mint Wash (`rgba(20, 184, 166, 0.2)`).
- Error / Flagged: 1px border `#F43F5E`, focus ring in warm coral wash (`rgba(244, 63, 94, 0.15)`).

### Checkboxes & Radio Buttons
- Crisp `1.125rem` square (checkbox, `0.375rem` radius) or circle (radio).
- Unchecked: 1.5px border `#94A3B8`, background `#FFFFFF`.
- Checked: Teal fill (`#0D9488`), pure white interior glyph. Interactive click targets expand to `2.75rem` (`44px`) via invisible hitboxes for clinical touchscreens.

### Cards & Clinical Vitals Tiles
- Background `#FFFFFF`, border `1px solid #E2E8F0`, rounded to `1rem` (`16px`).
- Internal hierarchy: Header region separated with light divider or pure whitespace; metric section uses `numerical-metric` typography accompanied by subtle trend arrows and contextual micro-labels.

### List Items & Diagnostic Tables
- Row height fixed to `3.5rem` (`56px`) with alternating hover highlight in `#F8FAFC`.
- Vertical borders omitted in favor of fine horizontal baseline rules (`#F1F5F9`).
- Numeric values automatically format using OpenType tabular figures (`font-variant-numeric: tabular-nums`).