# Aureva Wellness — backend

FastAPI service behind the website's contact form.

```
POST /api/contact  →  validate  →  SMTP  →  COMPANY_EMAIL  →  JSON response
GET  /api/health   →  service + SMTP configuration status
```

Full setup, SMTP guidance, API reference, testing and deployment live in the
[root README](../README.md). This file is the short version.

## Quick start

```bash
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then fill it in
uvicorn main:app --reload --port 8000
```

Open <http://127.0.0.1:8000/api/health>. If `smtp_configured` is `false`, the API
still validates requests but returns 500 instead of sending. Set
`SMTP_DRY_RUN=true` to test validation without credentials.

## Files

| File | Purpose |
|---|---|
| `main.py` | The entire API: config, CORS, rate limiting, model, error handlers, email, routes |
| `api/index.py` | Vercel entry point; re-exports `app` from `main.py`. Not used locally |
| `vercel.json` | Routes all paths to the function when deploying this folder to Vercel |
| `check_smtp.py` | Verifies SMTP credentials on their own. Run this before debugging the API |
| `test_api.py` | Fifteen Task 1 / Task 2 checks against a running server. Standard library only |


## Before you open an issue

1. `python check_smtp.py` — is it the mail server?
2. `curl http://127.0.0.1:8000/api/health` — is the API up and configured?
3. Read the uvicorn terminal. Real errors are logged there in full; the browser
   deliberately only ever sees one generic sentence.
