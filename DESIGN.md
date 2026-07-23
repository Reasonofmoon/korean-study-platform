# 국어 학습 플랫폼 디자인 시스템

## 0. Research Log

- Concrete reference: the supplied English-learning platform at commit `e9f22ca4e463f4471349c048aa48dd89b949b3cb` informed the editorial navigation, ordered lesson rows, and paper-and-ink material language. Its branding, copy, illustrations, and learning assets are excluded.
- Runtime extraction: skipped because the supplied source repository and its design contract provide the relevant implementation evidence; the new platform remains an original Korean-language design system.
- Imagen drafts: skipped because the project needs a text-first learning surface, not decorative artwork.

## 1. Atmosphere & Identity

This is a calm study desk: warm paper, dark ink, and clear editorial hierarchy. Its signature is the lesson ledger, an ordered list that makes the next Korean-learning task obvious without turning the site into a dashboard.

## 2. Color

| Role | Token | Value | Usage |
|---|---|---:|---|
| Page | `--paper` | `#faf8f3` | Main background |
| Surface | `--surface` | `#fffdf8` | Reading panels |
| Surface muted | `--surface-muted` | `#f1ede3` | Metadata and callouts |
| Ink | `--ink` | `#1a2b25` | Headings and body text |
| Ink muted | `--ink-muted` | `#52685d` | Supporting copy |
| Pine | `--pine` | `#1e5244` | Links, selected controls, focus |
| Pine dark | `--pine-dark` | `#0f2e25` | Header and button hover |
| Pine soft | `--pine-soft` | `#dcebe4` | Active filter background |
| Gold | `--gold` | `#a98632` | Kicker and restrained emphasis |
| Border | `--border` | `#d8d2c5` | Dividers and rows |
| Success | `--success` | `#236b4d` | Ready status |
| Graph night | `--graph-night` | `#0f0f1a` | Ontology canvas default |
| Graph night panel | `--graph-night-panel` | `#1a1a2e` | Ontology sidebar default |
| Graph node text | `--graph-node-text` | `#ffffff` / `#1a2b25` | Ontology node labels by theme |

Rules: accent color signals navigation or learning state, never decoration. No raw color may appear outside the token definitions.

## 3. Typography

Primary stack: `"Noto Sans KR", Pretendard, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif`.

| Level | Size | Weight | Line height | Use |
|---|---:|---:|---:|---|
| Display | `clamp(2rem, 4vw, 3.25rem)` | 700 | 1.15 | Home statement |
| H1 | `2rem` | 700 | 1.2 | Page title |
| H2 | `1.5rem` | 700 | 1.3 | Section title |
| H3 | `1.125rem` | 700 | 1.4 | Lesson row title |
| Body | `1rem` | 400 | 1.75 | Reading content |
| Small | `0.875rem` | 500 | 1.55 | Metadata |
| Kicker | `0.75rem` | 700 | 1.3 | Section labels |

## 4. Spacing & Layout

The base unit is 4px. Use `--space-1` (4px), `--space-2` (8px), `--space-3` (12px), `--space-4` (16px), `--space-5` (20px), `--space-6` (24px), `--space-8` (32px), `--space-10` (40px), `--space-12` (48px), and `--space-16` (64px). Content width is 1120px. The site collapses to one readable column below 760px.

## 5. Components

### Site navigation
- Structure: brand link, primary routes, compact route chips.
- States: default, hover, active, focus.
- Accessibility: `<nav>` landmark; current route has `aria-current="page"`.

### Learning-path card
- Structure: level label, title, purpose, route link.
- States: default, hover, focus.
- Layout: responsive grid on the home page, single-column on narrow screens.

### Filter chip
- Structure: native `<button>` with label and visible count.
- States: default, hover, selected, focus.
- Accessibility: `aria-pressed`; filtering only changes `hidden` state on matching lessons.

### Graph theme toggle
- Structure: native button in the Graphify search panel.
- States: dark default, light selected, hover, focus.
- Accessibility: `aria-pressed` announces the selected light state; the choice persists only in browser local storage.

### Lesson ledger row
- Structure: order, subject tag, title and summary, time/status, route link.
- States: default, hover, focus, empty.
- Layout: a bordered row rather than nested cards.

### Study sequence
- Structure: numbered ordered list of five learning steps.
- States: static content; links within retain visible focus.

## 6. Motion & Interaction

Hover and focus transitions use `150ms ease-out` and only transition color, border-color, transform, or opacity. Hover may lift a card by 1px. Reduced-motion users receive no transition. Filtering is instant and preserves document order.

## 7. Depth & Surface

Depth strategy is borders plus warm tonal shifts. Top-level paper panels may use one soft shadow; ledger rows use borders only and never nest a second raised card.

## 8. Accessibility Constraints & Accepted Debt

Target WCAG 2.2 AA: 4.5:1 body contrast, keyboard access for every control, visible 2px focus ring, semantic landmarks, and reduced-motion support.

| Item | Location | Why accepted | Exit |
|---|---|---|---|
| Persistent learner progress | Whole site | Static Hexo release has no account store | Add only with a privacy-reviewed account design |
| Audio narration | Lesson pages | No licensed or public-domain narration is bundled initially | Add per lesson only when source rights and accessibility transcript are ready |
