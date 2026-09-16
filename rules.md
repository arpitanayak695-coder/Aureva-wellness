# rules.md — hard rules for future changes

These are the constraints this project was built under. Break one and you are
building a different website.

## Design

1. **Preserve the reference design.** Section order, hero composition, card
   style, price card, guide circle, three-up stories and the footer watermark
   all come from the reference. Do not reorder or re-skin them.
2. **Keep the pink-and-white theme.** `--rose #F0709C` and `--rose-deep #E0356F`
   on cream and white. No dark mode, no second accent hue, no gradient washes
   beyond the two already in use.
3. **Do not redesign unnecessarily.** Change what the task asks for. If a fix
   needs a new component, build it from the existing tokens in `:root`.
4. **Keep the type pairing.** Fraunces for headings, Manrope for text. Adding a
   third family is a redesign.
5. **Never leave an image slot empty.** Every `img` points at a real local file
   with real `alt` text. No placeholder services, no empty `src`, no
   "add image here".

## Engineering

6. **The backend stays Python.** FastAPI + Uvicorn + Pydantic + smtplib. No
   Node, no Express, no swapping the API for a third-party form service.
7. **Frontend and backend stay separate.** The frontend is a static site that
   knows one thing about the backend: a URL in `config.js`. They deploy
   independently.
8. **Never expose SMTP secrets.** Credentials live in `.env` or the host's
   environment panel only. Nothing secret goes in any file the browser can
   download. `.env` is never committed.
9. **Validate every input server-side.** Client checks are a courtesy. The API
   treats every request as untrusted, checks required fields, types, lengths,
   email format and the programme allow-list, and rejects blank or
   whitespace-only values.
10. **Always answer in the JSON envelope.** `{"success": bool, "message": str}`
    with an optional `errors` object. Every path — success, validation, 405,
    429, 500 — uses it. No bare strings, no HTML error pages.
11. **Never leak internals.** No stack traces, no credential names, no host
    details in a response. Log the detail server-side, return one sentence.
12. **Maintain responsive design.** Anything new must hold from 320px up with no
    horizontal scroll. Use `clamp()` and the existing spacing variables rather
    than fixed pixels.
13. **Avoid unnecessary dependencies.** The frontend has none and should keep
    none. The backend has five, each doing a job the standard library does not.
14. **Do not claim untested features work.** Email delivery is "working" only
    after a message has actually landed in the inbox. If something has not been
    run, say so.

## Content

15. Keep the brand name **Aureva Wellness** consistent across pages, the email
    subject line and the documents.
16. Do not collect sensitive medical information in the form. Name, mobile,
    email, programme, date, time and a free-text message is the whole set.
