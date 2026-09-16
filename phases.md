# phases.md — how this project was built

## Phase 1 — Reference image analysis
Read the reference as a section inventory: nav pill, full-bleed hero with
floating chips, eyebrow + statement about block with stats, card row, image/text
consistency block with a thumbnail strip, membership block with a saturated pink
price card, brand watermark, circular guide portrait, three-up stories, footer
with link columns and a second watermark. Extracted the palette (rose on cream),
the light-serif heading voice, the pill-and-rounded-rectangle geometry and the
generous vertical rhythm. Recorded in `design.md`.

## Phase 2 — Website design and frontend development
Built the token system in `:root` first (colour, type, radius, shadow, shell,
section rhythm), then each section against the inventory from Phase 1. Original
SVG illustrations were generated and wired in as the sections were built, so no
slot was ever a placeholder. Card hover (lift + warm background + pink glow) was
implemented here, mirrored on `:focus-within`.

## Phase 3 — Contact Us page
A second page sharing `style.css`, the nav and the footer, adding `contact.css`
for the form panel. Seven required fields, the success panel and the error slots
were all built into the markup up front so JS only toggles state rather than
generating HTML.

## Phase 4 — Python backend setup
`backend/` with a virtual environment, pinned `requirements.txt`, `.env.example`,
`.gitignore`, the FastAPI app, CORS middleware and a `/api/health` endpoint used
throughout the rest of the work to confirm the service and its configuration.

## Phase 5 — Task 1, SMTP integration
`POST /api/contact` built end to end: form → fetch → FastAPI → validation →
smtplib → studio inbox → JSON → in-page success panel. Multipart plain+HTML
email, `Reply-To` set to the visitor, SSL on 465 and STARTTLS elsewhere,
20-second timeout. `SMTP_DRY_RUN` and `check_smtp.py` added so delivery can be
diagnosed separately from the API.

## Phase 6 — Task 2, validation and API security
Pydantic model with per-field constraints and custom validators (name pattern,
phone pattern, programme allow-list, date window, message length). Exception
handlers translate every failure into the same JSON envelope: 400 for validation
and malformed JSON, 405 for wrong methods, 429 for rate limiting, 500 for
anything unexpected — with the detail logged server-side and never returned.
CORS allow-list, security headers and a 16 KB body cap added.

## Phase 7 — Frontend API integration
`contact.js`: prevent default, collect and trim, validate locally, POST with
fetch, show a loading state, lock against double submission, render the API's
per-field errors, handle 400/405/429/500, handle network failure and timeout,
and reset the form only after a confirmed success.

## Phase 8 — Testing
Static verification in the build environment: Python compiled, JS syntax-checked,
HTML parsed for structure and for missing assets, CSS braces and custom
properties checked, and form field names compared against the Pydantic model.
`test_api.py` written to cover fifteen Task 1 / Task 2 cases over the running
API, plus a manual browser checklist in README section 13.

**Not done here:** no dependency install and no server run — the build
environment had no network. The live request cycle and real email delivery are
verified locally by the reader.

## Phase 9 — Deployment preparation
Static frontend with no build step; `config.js` isolates the API URL.
`vercel.json` and `api/index.py` for a Vercel Python deployment, with Render
documented as the recommended target for the API and the serverless caveats
spelled out. CORS configuration documented on both sides.

## Phase 10 — Final verification
Every asset path resolved, every label bound to an input, every documented file
present, and the limits of what was tested stated plainly in the README rather
than papered over.
