# memory.md — project memory

Read this first when returning to the project or handing it to another developer.

## Project overview

Aureva Wellness is a yoga and meditation studio site. One static frontend, one
Python API. The only dynamic behaviour on the whole site is the contact form:
it POSTs JSON to the API, the API validates it and emails the studio.

## Technologies

- Frontend: HTML5, CSS3 (custom properties, grid, `clamp()`), vanilla JS (Fetch).
  No build step, no bundler, no framework.
- Backend: Python 3.10+, FastAPI 0.115, Uvicorn, Pydantic v2, email-validator,
  python-dotenv, smtplib (stdlib).
- Assets: 22 original SVG illustrations in `frontend/assets/images/`.

## Project structure

See README section 4. The rules that matter:

- `style.css` owns the tokens in `:root`; `contact.css` only adds the form page
  and must not redefine a token.
- `config.js` is the single place the API URL is configured. It auto-selects the
  local API for localhost/LAN/file origins and `API_BASE_PRODUCTION` otherwise.
- `main.js` is shared by both pages; `contact.js` only runs where `#contactForm`
  exists.
- `backend/main.py` is the whole API. `backend/api/index.py` exists solely so
  Vercel can find an ASGI app; it imports and re-exports the same object.

## API details

`POST /api/contact` — body keys: `full_name`, `mobile`, `email`, `program`,
`preferred_date` (YYYY-MM-DD), `preferred_time` (HH:MM), `message`.
These names are identical in the HTML `name` attributes, the JS `FIELDS` array
and the Pydantic model. **If you rename one, rename all three.**

Responses: 200 success · 400 validation (`errors` map keyed by field) ·
405 wrong method · 413 oversized body · 429 rate limited · 500 mail failure.

`GET /api/health` reports `smtp_configured` and `dry_run` — the fastest way to
tell whether a 500 is a configuration problem.

## SMTP integration

`send_email()` picks SMTP_SSL for port 465 and STARTTLS otherwise, both with a
verified TLS context and a 20-second timeout. The message is multipart: plain
text plus an HTML version. `Reply-To` is set to the visitor's address so the
studio can reply straight from the notification. Every user value is
HTML-escaped before it enters the HTML part.

`SMTP_DRY_RUN=true` logs the email instead of sending it. It exists for testing
validation before credentials are available. It must be false in production —
`/api/health` will tell you if it is not.

## Environment variables

`SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM_EMAIL`,
`COMPANY_EMAIL`, `COMPANY_NAME`, `FRONTEND_ORIGIN`, `FRONTEND_ORIGIN_REGEX`
(optional), `SMTP_DRY_RUN`, `RATE_LIMIT_MAX`, `RATE_LIMIT_WINDOW_SECONDS`,
`LOG_LEVEL`. Documented in `.env.example`; `.env` is git-ignored.

Gmail requires an app password. The ordinary account password is always rejected.

## Deployment notes

Frontend: any static host (Vercel, Netlify, Cloudflare Pages), root directory
`frontend`, no build command.

Backend: Render / Railway / Fly with
`uvicorn main:app --host 0.0.0.0 --port $PORT`, root directory `backend`. Vercel
works via `api/index.py` + `vercel.json`, with the caveats in README section 15
(10s function limit, cold starts, rate limiter state resets).

After deploying: set `API_BASE_PRODUCTION` in `config.js`, and add the frontend's
exact origin to `FRONTEND_ORIGIN` on the backend. Both sides need updating — a
CORS error means you did one of them.

## Known limitations

- The rate limiter is in-process. Several workers or serverless instances each
  keep their own counters. Move it to Redis if that matters.
- No persistence: an enquiry exists only as an email. If you need a record,
  add a database write next to `send_email()`.
- The build environment where this project was written had no network access, so
  dependencies were never installed and the server was never started. Syntax,
  asset paths and field-name parity were verified statically; the live
  request/response cycle and real email delivery still need a local run.

## Future modification rules

1. Read `rules.md` before changing anything.
2. Any new form field must be added in four places: the HTML input, the `FIELDS`
   array in `contact.js`, the Pydantic model, and the email body builder.
3. New sections reuse the tokens in `:root` — never hard-code a hex value.
4. Never move a secret into the frontend, not even temporarily.
5. Re-run `python test_api.py` after touching `main.py`, and check the contact
   page at 320px after touching any CSS.
