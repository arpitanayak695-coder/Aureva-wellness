# design.md — Aureva Wellness

## 1. Reference image analysis

The reference is a single-column premium wellness landing page. What it actually
establishes, section by section:

| Region | Observed treatment |
|---|---|
| Navigation | Floating white pill, centred links, one filled pink CTA at the right |
| Hero | Full-bleed rounded panel, soft pink gradient sky, a centred seated illustration, small white "chips" floating around the figure, headline set low-left, supporting line to the right |
| About | Small pink eyebrow label, a large light-serif statement paragraph, a three-cell stat row, image to the right |
| Programmes | Centred two-line heading, a row of white cards: image on top, title, one line of copy |
| Consistency | Image left, heading + copy right, a strip of three tall thumbnails underneath |
| Membership | Text and CTA left, a saturated pink card right with pill-shaped feature chips and a large price |
| Watermark | The brand name set enormous and very low-contrast behind the lower sections |
| Guides | Circular portrait, name, role, a pill button, a large-number credential |
| Stories | Three-up row: quote card, image, quote card; each with a numeric rating badge |
| Footer | Large "stay close" heading, link columns, a figure illustration, brand watermark |

Everything above is reproduced. Nothing else was added.

## 2. Colour

| Token | Hex | Role |
|---|---|---|
| `--cream` | `#FFF7FA` | Page background |
| `--white` | `#FFFFFF` | Cards, nav, form panel |
| `--blush` | `#FFE6EF` | Alternating section tint |
| `--rose` | `#F0709C` | Primary accent, gradient start |
| `--rose-deep` | `#E0356F` | Buttons, links, focus, price card |
| `--ink` | `#2C1B23` | Body text — a warm near-black, never pure #000 |
| `--ink-soft` | `#7C6270` | Secondary text |

Two values carry the theme: the rose pair. Sections alternate cream → blush →
cream → blush so the page breathes without introducing a third hue. There is no
dark variant, by design.

## 3. Typography

- **Fraunces**, weight 300, for every heading and for the statement paragraph,
  large numerals and the price. A soft-contrast serif; it supplies the "premium
  but calm" register the reference leans on.
- **Manrope** for body copy, labels, buttons and form fields.
- Scale is fluid via `clamp()`: h1 `2.1–4.1rem`, h2 `1.75–2.9rem`, body `15–17px`.
- Headings are sentence case with a tight `-0.015em` letter-spacing and `1.12`
  line-height. Measure is capped near 46 characters on lede text.
- Both families fall back to Georgia and the system sans if Google Fonts is
  unreachable, so the page never loses its shape offline.

## 4. Layout

- Content sits in a `1180px` shell with a fluid gutter (`18–48px`).
- Vertical rhythm comes from one variable, `--section-y` (`64–120px`).
- Two-column sections use asymmetric `minmax()` fractions, not a rigid 50/50 —
  the reference consistently gives more room to whichever side carries the text.
- The hero is the exception: a full-bleed rounded panel that reaches wider than
  the shell, with the headline block below it rather than overlaid, which keeps
  the type legible at every width.

## 5. UI/UX decisions

- One sticky element (the nav pill) and one bold element per screen. Boldness is
  spent on the pink membership card; everything around it is quiet.
- Buttons are pills in three weights: filled gradient (primary), outlined
  (secondary), white-on-pink (inside the price card).
- Copy is written for a real studio — a timetable, a rupee price, an Odisha
  address — rather than lorem-flavoured marketing.
- Focus is always visible (`2.5px` rose outline, 3px offset), skip link included,
  and `prefers-reduced-motion` disables every transition.

## 6. Card hover effect

Required behaviour, implemented on `.card`:

```css
.card::after   { radial-gradient pink glow, opacity 0, z-index -1 }
.card:hover    { transform: translateY(-8px); background:#FFF6FA; box-shadow: glow }
.card:hover::after { opacity: 1 }
```

- Lift: 8px, `cubic-bezier(.22,.68,.32,1)` over 350ms.
- Background: white → `#FFF6FA`, a barely-there warm shift.
- Glow: a radial pink gradient on a pseudo-element behind the content, faded in,
  so nothing under the card is repainted and text contrast is untouched.
- `:focus-within` mirrors `:hover`, so keyboard users get the same feedback.

## 7. Contact page design

Same tokens, same nav and footer, two columns: story on the left (eyebrow,
heading, illustration, studio facts), form panel on the right as a white card
with a soft shadow. Fields are `#FFF9FB` with a hairline rose border, rounded to
22px to echo the cards. Errors turn the border red and print one sentence below
the field; the success state replaces the entire form with a pink gradient panel
so there is no doubt the request went through. On one column the story stacks
above the form.

## 8. Responsive design

Breakpoints at 980px (two columns collapse), 820px (nav becomes a toggle,
decorative hero chips are hidden), 640px (stories and footer go single column,
stat dividers drop) and 360px (remaining chips hidden, buttons tighten).

Fluid type and spacing mean those breakpoints only handle structure, not size.
`overflow-x: hidden` on the body plus `width: min(100% - gutters, shell)` keeps
the page free of horizontal scroll from 320px upward.

## 9. Imagery

All 22 illustrations are original SVG, hand-built from primitives in the palette
above: gradient sky, sun disc, concentric rings, soft horizon, and figures in
sukhasana, vrikshasana, balasana and paschimottanasana. SVG was chosen over
raster because the whole set weighs about 100 KB, stays sharp on any display,
and shares the exact CSS palette. Regenerate or tweak them with the script that
produced them if you want different poses or crops.
