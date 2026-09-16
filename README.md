# Aureva Wellness — yoga & wellness website

A complete, working yoga studio website: a static frontend (HTML / CSS / vanilla JS)
and a separate Python API (FastAPI) that validates the contact form and delivers it
to the studio inbox over SMTP.

```
Contact form  →  fetch POST  →  FastAPI  →  validation  →  SMTP  →  company inbox
                                                        →  JSON  →  in-page success panel
```

---

## 1. Project overview

| | |
|---|---|
| Brand | Aureva Wellness |
| Frontend | Static site, no build step, no framework |
| Backend | Python 3.10+ / FastAPI / Uvicorn / Pydantic v2 / smtplib |
| API | `POST /api/contact`, `GET /api/health` |
| Theme | Soft pink and white, per the supplied reference design |

---

## 2. Features

- Responsive landing page: hero, about + stats, six class cards, consistency section,
  membership + price card, guides, member stories, footer.
- Card hover: lifts slightly, background warms, a soft pink glow fades in behind it.
- Separate contact page with a seven-field request form.
- Client-side validation, loading state, duplicate-submit lock, and an in-page
  success panel (not a JS `alert`).
- Server-side validation with per-field error messages returned as JSON.
- CORS restricted to configured origins, in-memory rate limiting, security headers,
  body-size cap, and error handling that never leaks credentials or stack traces.
- All artwork is original SVG, stored locally in `frontend/assets/images/`.

---

## 3. Technologies

**Frontend** — HTML5, CSS3 (custom properties, `clamp()`, grid, flexbox), vanilla JS
with the Fetch API. Fonts: Fraunces + Manrope from Google Fonts, with system fallbacks.

**Backend** — Python 3.10+, FastAPI, Uvicorn, Pydantic v2, `email-validator`,
`python-dotenv`, and `smtplib` from the standard library.

---

## 4. Project structure

```
yoga-wellness-website/
│
├── frontend/
│   ├── index.html            landing page
│   ├── contact.html          contact page
│   ├── style.css             design tokens + all landing styles
│   ├── contact.css           contact page only, loaded after style.css
│   ├── config.js             API base URL — the one file to edit when deploying
│   ├── main.js               nav, sticky header, footer year
│   ├── contact.js            form validation, fetch, states
│   └── assets/
│       ├── images/           22 original SVG illustrations
│       └── videos/           empty; drop a studio clip here if you add one
│
├── backend/
│   ├── main.py               the API (FastAPI app)
│   ├── api/index.py          Vercel serverless entry point (re-exports `app`)
│   ├── check_smtp.py         standalone SMTP credential check
│   ├── test_api.py           Task 1 + Task 2 test script (stdlib only)
│   ├── requirements.txt
│   ├── vercel.json
│   ├── .env                  your real values — never commit
│   ├── .env.example
│   ├── .gitignore
│   └── README.md
│
├── README.md      this file
├── design.md      design analysis and decisions
├── memory.md      project memory / modification rules
├── phases.md      the ten build phases
├── PRD.md         product requirements
└── rules.md       hard rules for future changes
```

Two files are outside the originally requested list and both earn their place:
`frontend/config.js` (one place to change the API URL, so no code edits at deploy
time) and `backend/check_smtp.py` + `backend/test_api.py` (how you verify Task 1
and Task 2 without guesswork).

---

## 5. Install Python

Python 3.10 or newer. Check with:

```bash
python --version      # Windows
python3 --version     # macOS / Linux
```

If it is missing, install from <https://www.python.org/downloads/> and tick
**Add Python to PATH** on Windows.

---

## 6. Virtual environment

```bash
cd yoga-wellness-website/backend

python -m venv .venv            # Windows
.venv\Scripts\activate

python3 -m venv .venv           # macOS / Linux
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. Use `deactivate` to leave.

---

## 7. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 8. Environment variables

```bash
cp .env.example .env      # macOS / Linux
copy .env.example .env    # Windows
```

| Variable | What it is |
|---|---|
| `SMTP_HOST` | Mail server hostname, e.g. `smtp.gmail.com` |
| `SMTP_PORT` | `587` for STARTTLS, `465` for SSL |
| `SMTP_USERNAME` | The mailbox that logs in |
| `SMTP_PASSWORD` | App password / SMTP key — **not** your account password |
| `SMTP_FROM_EMAIL` | The "From" address; usually must match the username |
| `COMPANY_EMAIL` | Where enquiries land |
| `COMPANY_NAME` | Display name on the From header |
| `FRONTEND_ORIGIN` | Comma-separated origins allowed to call the API, no trailing slash |
| `FRONTEND_ORIGIN_REGEX` | Optional regex for preview URLs |
| `SMTP_DRY_RUN` | `true` logs the email instead of sending it — test mode only |
| `RATE_LIMIT_MAX` / `RATE_LIMIT_WINDOW_SECONDS` | Requests allowed per IP per window |

`.env` is listed in `.gitignore`. Keep it that way — it holds a password.

---

## 9. SMTP configuration

### Gmail (quickest for a test)

1. Turn on 2-Step Verification on the Google account.
2. Go to <https://myaccount.google.com/apppasswords> and create an app password.
   You get 16 characters; paste them into `SMTP_PASSWORD` (spaces are fine to remove).
3. Fill in:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=yourstudio@gmail.com
SMTP_PASSWORD=xxxxxxxxxxxxxxxx
SMTP_FROM_EMAIL=yourstudio@gmail.com
COMPANY_EMAIL=yourstudio@gmail.com
```

Your normal Google password will always be rejected — an app password is required.

### Other providers

| Provider | Host | Port |
|---|---|---|
| Outlook / Microsoft 365 | `smtp.office365.com` | 587 |
| Zoho (India) | `smtp.zoho.in` | 465 |
| Brevo | `smtp-relay.brevo.com` | 587 |
| SendGrid | `smtp.sendgrid.net` | 587 (username is literally `apikey`) |

For a real business site, a transactional provider (Brevo, SendGrid, Resend, Mailgun)
delivers more reliably than a personal Gmail account and will not lock you out for volume.

### Verify the credentials before anything else

```bash
python check_smtp.py          # connects and logs in
python check_smtp.py --send   # also sends a real test email
```

No credential is printed by that script.

---

## 10. Run the backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

- API root: <http://127.0.0.1:8000/>
- Health: <http://127.0.0.1:8000/api/health>
- Interactive docs: <http://127.0.0.1:8000/docs>

---

## 11. Run the frontend

**VS Code Live Server (recommended).** Install the Live Server extension, right-click
`frontend/index.html` → *Open with Live Server*. It serves on `http://127.0.0.1:5500`,
which is already in the default `FRONTEND_ORIGIN`.

**Python's own server** works too:

```bash
cd frontend
python -m http.server 5500
```
Then open <http://127.0.0.1:5500/index.html>.

**Opening the file directly** (`file:///…/index.html`) renders the site fine, but the
browser sends `Origin: null` on the form POST and CORS will block it. Use a local
server when you want to test the form.

`config.js` auto-detects localhost and points at `http://127.0.0.1:8000`, so nothing
needs editing for local work.

---

## 12. API documentation

### `POST /api/contact`

Request body (`application/json`):

```json
{
  "full_name": "Ritu Panda",
  "mobile": "+91 90000 00000",
  "email": "ritu@example.com",
  "program": "Beginner yoga",
  "preferred_date": "2026-10-02",
  "preferred_time": "07:00",
  "message": "I am new to yoga and would like to join the sunrise class."
}
```

Rules: all fields required and non-blank; name 2–80 chars (letters, spaces, `.`, `'`, `-`);
mobile 8–20 chars matching a phone pattern; valid email; programme must be one of the
seven listed; date today-or-later and within twelve months; time `HH:MM`;
message 10–1000 chars. Unknown fields are ignored.

**200**
```json
{ "success": true, "message": "Your request has been submitted successfully." }
```

**400**
```json
{
  "success": false,
  "message": "Please correct the highlighted fields.",
  "errors": { "email": "Please enter a valid email address." }
}
```

**405** — wrong method · **413** — body over 16 KB · **429** — rate limited ·
**500** — mail could not be sent (generic message only).

### `GET /api/health`

```json
{ "success": true, "status": "ok", "smtp_configured": true, "dry_run": false }
```

---

## 13. Testing

**Automated (Task 1 + Task 2).** With the API running:

```bash
cd backend
python test_api.py
```

Fifteen checks: valid submission, invalid/empty email, whitespace-only values,
missing field, min/max lengths, wrong types, unknown programme, past date,
malformed JSON, empty body, GET and PUT → 405. Run it three times in a row and later
valid submissions should return 429, which proves rate limiting works.

To exercise validation before SMTP exists, set `SMTP_DRY_RUN=true` in `.env` and
restart — case 1 then passes and the email is written to the terminal instead.

**Manual, in the browser.** Open the contact page and check:

1. Submit empty → field errors appear, nothing is sent.
2. Enter `abc` in email → "Please enter a valid email address."
3. Fill everything correctly → button shows "Sending…", then the pink success panel
   replaces the form and the email arrives in `COMPANY_EMAIL`.
4. Double-click the button → only one request goes out (check the Network tab).
5. Stop the backend and submit → the "could not reach the studio server" message.
6. Resize to 320 px → no horizontal scrolling anywhere.
7. Hover a class card → it lifts, warms, and a pink glow appears.
8. Click "Contact us" anywhere → the contact page opens.

**What I could not test for you:** my build environment has no network access, so
dependencies could not be installed and the server was never started. Python, JS,
HTML and CSS were syntax-checked, every asset path was verified to resolve, and the
form field names were checked against the API model — but the running request/response
cycle and real email delivery are yours to confirm with the steps above. Do not treat
email delivery as working until you have seen a message land in the inbox.

---

## 14. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| "could not reach the studio server" | The API is not running, or the port differs. Open `/api/health` in a browser. |
| CORS error in the console | The page's origin is not in `FRONTEND_ORIGIN`. Add it exactly — scheme, host, port, no trailing slash — and restart uvicorn. |
| Works on `127.0.0.1` but not `localhost` | Different origins to the browser. Both are in the default list; keep both. |
| 500 on a valid form | SMTP. Run `python check_smtp.py` and read the uvicorn log. |
| `SMTPAuthenticationError` | Gmail account password used instead of an app password, or 2-Step Verification is off. |
| Email never arrives | Check spam; confirm `COMPANY_EMAIL`; some hosts block outbound port 587 — try 465. |
| 429 during testing | You hit the rate limit. Wait, or raise `RATE_LIMIT_MAX`, or restart the server. |
| Fonts look plain | Google Fonts is blocked or offline; the fallback stack is in use. Harmless. |
| Form opens as `file://` and fails | Serve the frontend over http (Live Server). |

---

## 15. Deployment

### Recommended: frontend on Vercel, backend on Render

Vercel's Python support is serverless. It works for this API, but a long-lived
server is a better fit for SMTP: no cold start on the first enquiry of the day,
outbound port 587 is reliable, and the in-memory rate limiter actually holds state.

**Backend on Render (free tier):**

1. Push the repo to GitHub (`.env` stays out, thanks to `.gitignore`).
2. Render → New → Web Service → pick the repo → **Root Directory** `backend`.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add every variable from `.env.example` under *Environment*.
6. Deploy and open `https://your-service.onrender.com/api/health`.

Railway and Fly.io work the same way with the same two commands.

**Frontend on Vercel:**

1. Vercel → New Project → same repo → **Root Directory** `frontend`.
2. Framework preset: *Other*. No build command, no output directory.
3. Deploy, then edit `frontend/config.js` → `API_BASE_PRODUCTION` = your Render URL,
   and push.
4. Set `FRONTEND_ORIGIN=https://your-site.vercel.app` on Render and redeploy.

Netlify, Cloudflare Pages or GitHub Pages serve the frontend equally well.

### If you want the backend on Vercel too

`backend/api/index.py` and `backend/vercel.json` are already in place.

1. Create a second Vercel project from the same repo with **Root Directory** `backend`.
2. Vercel detects `api/index.py` and runs the FastAPI app as a serverless function;
   `vercel.json` routes every path to it.
3. Add the same environment variables in *Project Settings → Environment Variables*.
4. Point `API_BASE_PRODUCTION` at that deployment and add its origin to `FRONTEND_ORIGIN`.

Caveats worth knowing before you choose this: functions are limited to 10 seconds on
the Hobby plan (a slow SMTP handshake can exceed that), each invocation may be a fresh
instance so the rate limiter resets, and some SMTP hosts throttle connections from
shared serverless IPs. If enquiries start failing intermittently, move the API to Render.

Never deploy the frontend and backend as one service; the frontend must stay a
static site and the backend must keep its secrets server-side.

---

## 16. Security notes

- Secrets live only in `.env` / the host's environment panel. Nothing sensitive is in
  any file the browser downloads — `config.js` holds a URL and nothing else.
- CORS is an allow-list. Do not set it to `*` on a public deployment.
- Every input is validated server-side; client-side checks are a convenience only.
- All values are HTML-escaped before going into the email body, so a pasted
  `<script>` tag cannot execute in whoever reads the message.
- Unexpected exceptions are logged in full server-side and returned to the browser as
  one generic sentence: no stack traces, no variable names, no host details.
- Rate limiting is per-IP and in-memory. Behind several workers or on serverless,
  move it to Redis or put Cloudflare in front.
- Responses carry `X-Content-Type-Options`, `Referrer-Policy` and `X-Frame-Options`,
  and request bodies over 16 KB are rejected.
- If a credential ever lands in a commit, rotate it. Removing the line is not enough.
