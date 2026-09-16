# PRD.md — Aureva Wellness website

## 1. Project overview

A marketing website for a yoga and meditation studio, plus a contact channel that
turns a web form into an email in the studio's inbox. The site is static; the only
server-side component is a small Python API that validates enquiries and sends them
on. Frontend and backend are separate applications with separate deployments.

## 2. Goals

1. Present the studio credibly enough that a first-time visitor books a class.
2. Get an enquiry from the browser into the studio inbox reliably, with every field
   the studio needs to reply.
3. Reject bad or hostile input at the server, not just in the browser.
4. Keep credentials out of anything the browser can download.
5. Stay maintainable: no build step, no framework churn, readable by one developer
   six months from now.

## 3. Target users

- **Prospective member**, usually on a phone, comparing two or three studios. Wants
  to know what is taught, by whom, when, and what it costs — in under a minute.
- **Returning member**, checking the timetable or booking a personal session.
- **Studio owner**, who receives the enquiries and must be able to reply from the
  notification email without re-typing an address.
- **Developer/maintainer**, who needs to configure SMTP, deploy both halves and
  extend the form without reading every file.

## 4. Functional requirements

| # | Requirement |
|---|---|
| F1 | Landing page with hero, about + statistics, six class cards, consistency section, membership with pricing, guides, member stories and footer |
| F2 | Class cards lift, warm and glow on hover, and on keyboard focus |
| F3 | Every "Contact us" control opens the dedicated contact page |
| F4 | Contact form collects full name, mobile, email, programme, preferred date, preferred time and message — all required |
| F5 | Submitting POSTs JSON to `POST /api/contact` |
| F6 | The API validates the payload and returns per-field errors on failure |
| F7 | On success the API sends an email to the configured company address |
| F8 | The browser shows an in-page success panel, not a JS alert, and clears the form only then |
| F9 | Loading state during the request; repeat submissions blocked while in flight |
| F10 | Validation errors, server errors and network failures each get a distinct, actionable message |
| F11 | `GET /api/health` reports service and SMTP configuration status |

## 5. Non-functional requirements

- **Responsive** from 320px to large desktop with no horizontal overflow.
- **Accessible**: semantic landmarks, labelled inputs, visible focus, skip link,
  `aria-live` error slots, `prefers-reduced-motion` honoured, text contrast at or
  above WCAG AA on the pink palette.
- **Performance**: no framework, no bundler; total illustration payload around
  100 KB of SVG; images below the fold are lazy-loaded.
- **Portability**: the frontend runs from any static host or VS Code Live Server;
  the backend runs anywhere Python 3.10+ runs.
- **Reliability**: a failed email never silently reports success.
- **Maintainability**: design tokens in one block; API URL in one file; field names
  identical across HTML, JS and Python.

## 6. Frontend requirements

HTML5, CSS3 and vanilla JavaScript only; no frameworks, no runtime dependencies.
Two pages sharing `style.css`, `main.js`, the nav and the footer. Fluid type and
spacing via `clamp()`. All imagery local, with meaningful `alt` text. The Fetch API
for the single network call. Field names must match the API contract exactly.

## 7. Backend requirements

Python 3.10+, FastAPI, Uvicorn, Pydantic v2, python-dotenv, smtplib. Configuration
exclusively from environment variables. Structured logging to the server, never to
the client. Pinned dependency versions. Startup must not require anything outside
`requirements.txt` and `.env`.

## 8. API requirements

- `POST /api/contact` accepts `application/json` with the seven fields.
- `GET /api/health` returns service status.
- Every response is JSON in the shape `{"success": bool, "message": str}`, with an
  `errors` object on validation failures.
- Status codes: 200 success, 400 validation or malformed JSON, 405 wrong method,
  413 oversized body, 429 rate limited, 500 internal failure.
- Unknown fields are ignored rather than rejected.
- CORS restricted to a configured allow-list.

## 9. SMTP requirements

Authenticated submission over TLS — implicit SSL on port 465, STARTTLS otherwise —
with a connection timeout. Multipart plain-text and HTML message containing every
submitted field and a timestamp. `Reply-To` set to the enquirer so the studio can
reply directly. Host, port, credentials, sender and recipient all from environment
variables. A dry-run mode for testing without credentials. A standalone script to
verify credentials independently of the API.

## 10. Validation

| Field | Rule |
|---|---|
| `full_name` | required, 2–80 chars, letters plus space `.` `'` `-` (Latin and Devanagari) |
| `mobile` | required, 8–20 chars, phone pattern, optional leading `+` |
| `email` | required, valid address (`email-validator`), rejects empty and malformed |
| `program` | required, must match one of the seven offered programmes |
| `preferred_date` | required, ISO date, today or later, within twelve months |
| `preferred_time` | required, `HH:MM` |
| `message` | required, 10–1000 chars |

All string fields are stripped before validation, so whitespace-only values fail as
empty. Missing fields, wrong types, missing bodies and malformed JSON all return 400
in the standard envelope. The same rules exist in the browser for fast feedback, but
the server is the authority.

## 11. Security

No secret reachable from the browser. CORS allow-list rather than a wildcard.
Per-IP rate limiting with a configurable window. 16 KB request body cap.
`X-Content-Type-Options`, `Referrer-Policy` and `X-Frame-Options` on every response.
All user values HTML-escaped before entering the email body. Generic 500 messages
with full detail logged server-side only. `.env` git-ignored, `.env.example`
committed with empty values.

## 12. Success criteria

1. The site renders correctly from 320px to 1920px with no horizontal scroll.
2. A complete, valid submission produces a 200, an in-page success panel, and an
   email in the company inbox containing all seven fields.
3. Each validation case in `test_api.py` returns the documented status code and,
   where applicable, a per-field message the user can act on.
4. A wrong HTTP method returns 405; malformed JSON returns 400; both in the standard
   envelope.
5. No response, page source or committed file contains a credential or a stack trace.
6. Stopping the backend produces a clear "cannot reach the server" message rather
   than a silent failure or a false success.
7. Card hover shows lift, warmth and glow, and the same on keyboard focus.

## 13. Deployment requirements

Frontend deployable as a static site with no build command (root directory
`frontend`). Backend deployable either as a long-running ASGI service
(`uvicorn main:app --host 0.0.0.0 --port $PORT`, recommended) or as a Vercel Python
function via `api/index.py` and `vercel.json`. All configuration through the host's
environment variables. The frontend's production API URL configurable in one file.
The backend's allowed origin updated to the deployed frontend. The two must remain
independently deployable.
