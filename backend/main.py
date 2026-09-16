from __future__ import annotations

import logging
import os
import re
import smtplib
import ssl
import time
from datetime import date, datetime, time as time_cls
from email.message import EmailMessage
from email.utils import formataddr
from html import escape
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator
from starlette.exceptions import HTTPException as StarletteHTTPException

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s  %(levelname)-8s %(name)s  %(message)s",
)
log = logging.getLogger("aureva.api")


SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "587") or 587)
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "").strip()
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "").strip()
COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "").strip()
COMPANY_NAME = os.getenv("COMPANY_NAME", "Aureva Wellness").strip()


FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5500").strip()
ALLOWED_ORIGINS: List[str] = [o.strip() for o in FRONTEND_ORIGIN.split(",") if o.strip()]


SMTP_DRY_RUN = os.getenv("SMTP_DRY_RUN", "false").strip().lower() in {"1", "true", "yes"}

RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "5") or 5)
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "900") or 900)

MAX_BODY_BYTES = 16 * 1024  # a contact form never needs more than this

PHONE_RE = re.compile(r"^[+(]?[0-9][0-9\s\-()]{7,19}$")
NAME_RE = re.compile(r"^[A-Za-z\u00C0-\u024F\u0900-\u097F' .\-]{2,80}$")

PROGRAMS = {
    "Beginner yoga",
    "Meditation",
    "Stress relief",
    "Flexibility & mobility",
    "Mindfulness",
    "Personal wellness session",
    "Not sure yet — please advise",
}


app = FastAPI(
    title="Aureva Wellness Contact API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=os.getenv("FRONTEND_ORIGIN_REGEX") or None,
    allow_credentials=False,          # the form sends no cookies
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
    max_age=600,
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Adds conservative response headers and caps the request body size."""
    length = request.headers.get("content-length")
    if length and length.isdigit() and int(length) > MAX_BODY_BYTES:
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={"success": False, "message": "That request is too large."},
        )
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    return response


_hits: Dict[str, List[float]] = {}


def rate_limited(client_ip: str) -> bool:
    now = time.time()
    window = [t for t in _hits.get(client_ip, []) if now - t < RATE_LIMIT_WINDOW]
    if len(window) >= RATE_LIMIT_MAX:
        _hits[client_ip] = window
        return True
    window.append(now)
    _hits[client_ip] = window
    if len(_hits) > 5000:               # keep the dict from growing forever
        for ip in [k for k, v in _hits.items() if not v or now - v[-1] > RATE_LIMIT_WINDOW]:
            _hits.pop(ip, None)
    return False


class ContactRequest(BaseModel):
    """The shape of a valid POST /api/contact body."""

    model_config = {"extra": "ignore", "str_strip_whitespace": True}

    full_name: str = Field(min_length=2, max_length=80)
    mobile: str = Field(min_length=8, max_length=20)
    email: EmailStr
    program: str = Field(min_length=2, max_length=60)
    preferred_date: date
    preferred_time: time_cls
    message: str = Field(min_length=10, max_length=1000)

    @field_validator("full_name")
    @classmethod
    def check_name(cls, v: str) -> str:
        if not NAME_RE.match(v):
            raise ValueError("Please enter your name using letters only.")
        return v

    @field_validator("mobile")
    @classmethod
    def check_mobile(cls, v: str) -> str:
        if not PHONE_RE.match(v):
            raise ValueError("Please enter a valid mobile number, for example +91 90000 00000.")
        return v

    @field_validator("program")
    @classmethod
    def check_program(cls, v: str) -> str:
        if v not in PROGRAMS:
            raise ValueError("Please choose one of the listed programmes.")
        return v

    @field_validator("preferred_date")
    @classmethod
    def check_date(cls, v: date) -> date:
        today = date.today()
        if v < today:
            raise ValueError("Please choose today or a future date.")
        if (v - today).days > 365:
            raise ValueError("Please choose a date within the next twelve months.")
        return v

    @field_validator("message")
    @classmethod
    def check_message(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Please tell us what you are looking for.")
        return v


FRIENDLY: Dict[str, str] = {
    "full_name": "Please enter your full name (2–80 characters).",
    "mobile": "Please enter a valid mobile number, for example +91 90000 00000.",
    "email": "Please enter a valid email address.",
    "program": "Please choose a programme.",
    "preferred_date": "Please choose a valid date (YYYY-MM-DD).",
    "preferred_time": "Please choose a valid time (HH:MM).",
    "message": "Please write between 10 and 1000 characters.",
}


def collect_errors(exc: ValidationError | RequestValidationError) -> Dict[str, str]:
    """Turns pydantic errors into {field: sentence} without leaking internals."""
    out: Dict[str, str] = {}
    for err in exc.errors():
        loc = [p for p in err.get("loc", ()) if p not in ("body",)]
        field = str(loc[0]) if loc else "form"
        if field in out:
            continue
        msg = err.get("msg", "")
        if err.get("type") == "value_error" and msg.startswith("Value error, "):
            out[field] = msg.replace("Value error, ", "", 1)
        elif field in FRIENDLY:
            out[field] = FRIENDLY[field]
        else:
            out[field] = "Please check this field."
    return out


@app.exception_handler(RequestValidationError)
async def on_validation_error(request: Request, exc: RequestValidationError):
    errors = collect_errors(exc)
    if any(e.get("type") in {"json_invalid", "missing"} and not e.get("loc", ())[1:]
           for e in exc.errors()):
        # Body missing entirely or not parseable as JSON.
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": "The request body must be valid JSON.",
                "errors": errors,
            },
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "message": "Please correct the highlighted fields.",
            "errors": errors,
        },
    )


@app.exception_handler(StarletteHTTPException)
async def on_http_error(request: Request, exc: StarletteHTTPException):
    if exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        message = "That HTTP method is not allowed on this endpoint. Use POST."
    elif exc.status_code == status.HTTP_404_NOT_FOUND:
        message = "That endpoint does not exist."
    else:
        message = exc.detail if isinstance(exc.detail, str) else "Request failed."
    payload: Dict[str, Any] = {"success": False, "message": message}
    return JSONResponse(status_code=exc.status_code, content=payload,
                        headers=getattr(exc, "headers", None))


@app.exception_handler(Exception)
async def on_unexpected_error(request: Request, exc: Exception):
    # Full detail to the server log, nothing sensitive to the caller.
    log.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Something went wrong on our side. Please try again shortly.",
        },
    )


def smtp_configured() -> bool:
    return all([SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD,
                SMTP_FROM_EMAIL, COMPANY_EMAIL])


def build_email(data: ContactRequest) -> EmailMessage:
    when = f"{data.preferred_date.isoformat()} at {data.preferred_time.strftime('%H:%M')}"

    plain = (
        "New class request from the Aureva website\n"
        "----------------------------------------\n"
        f"Name      : {data.full_name}\n"
        f"Mobile    : {data.mobile}\n"
        f"Email     : {data.email}\n"
        f"Programme : {data.program}\n"
        f"Preferred : {when}\n"
        f"Received  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "Message\n-------\n"
        f"{data.message}\n"
    )

    html = f"""\
<html><body style="margin:0;background:#FFF7FA;padding:24px;
  font-family:Segoe UI,Helvetica,Arial,sans-serif;color:#2C1B23;">
  <div style="max-width:560px;margin:0 auto;background:#fff;border-radius:18px;
       padding:26px;box-shadow:0 10px 30px rgba(199,77,127,.12);">
    <h2 style="margin:0 0 4px;font-weight:500;color:#E0356F;">New class request</h2>
    <p style="margin:0 0 18px;font-size:13px;color:#7C6270;">From the Aureva Wellness website</p>
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr><td style="padding:6px 0;color:#7C6270;">Name</td><td><strong>{escape(data.full_name)}</strong></td></tr>
      <tr><td style="padding:6px 0;color:#7C6270;">Mobile</td><td>{escape(data.mobile)}</td></tr>
      <tr><td style="padding:6px 0;color:#7C6270;">Email</td><td>{escape(str(data.email))}</td></tr>
      <tr><td style="padding:6px 0;color:#7C6270;">Programme</td><td>{escape(data.program)}</td></tr>
      <tr><td style="padding:6px 0;color:#7C6270;">Preferred</td><td>{escape(when)}</td></tr>
    </table>
    <p style="margin:18px 0 6px;color:#7C6270;font-size:13px;">Message</p>
    <p style="margin:0;white-space:pre-wrap;line-height:1.6;">{escape(data.message)}</p>
  </div>
</body></html>"""

    msg = EmailMessage()
    msg["Subject"] = f"[Aureva] {data.program} request from {data.full_name}"
    msg["From"] = formataddr((COMPANY_NAME, SMTP_FROM_EMAIL or SMTP_USERNAME))
    msg["To"] = COMPANY_EMAIL
    msg["Reply-To"] = str(data.email)
    msg.set_content(plain)
    msg.add_alternative(html, subtype="html")
    return msg


def send_email(msg: EmailMessage) -> None:
    """Delivers through SMTP. Raises on failure; the caller answers with 500."""
    if SMTP_DRY_RUN:
        log.warning("SMTP_DRY_RUN is on — email not sent. Subject: %s", msg["Subject"])
        log.info("\n%s", msg.get_body(preferencelist=("plain",)).get_content())
        return

    context = ssl.create_default_context()
    if SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=20) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)



@app.get("/api/health")
async def health() -> Dict[str, Any]:
    """Cheap check that the API is up and whether email is ready to send."""
    return {
        "success": True,
        "status": "ok",
        "smtp_configured": smtp_configured(),
        "dry_run": SMTP_DRY_RUN,
    }


@app.post("/api/contact")
async def contact(payload: ContactRequest, request: Request):
    client_ip = (request.headers.get("x-forwarded-for", "").split(",")[0].strip()
                 or (request.client.host if request.client else "unknown"))

    if rate_limited(client_ip):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "success": False,
                "message": "Too many requests from this device. Please try again later.",
            },
        )

    if not smtp_configured() and not SMTP_DRY_RUN:
        # Misconfiguration is our problem, not the visitor's: log the detail,
        # return a generic 500 without naming any variable or credential.
        log.error("SMTP is not configured — set the SMTP_* and COMPANY_EMAIL variables.")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "We could not send your request just now. "
                           "Please try again shortly or call the studio.",
            },
        )

    try:
        send_email(build_email(payload))
    except smtplib.SMTPAuthenticationError:
        log.exception("SMTP authentication failed — check username/app password.")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False,
                     "message": "We could not send your request just now. Please try again shortly."},
        )
    except (smtplib.SMTPException, OSError):
        log.exception("SMTP delivery failed.")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False,
                     "message": "We could not send your request just now. Please try again shortly."},
        )

    log.info("Contact request delivered for %s (%s)", payload.full_name, payload.program)
    return {
        "success": True,
        "message": "Your request has been submitted successfully.",
    }


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"success": True, "message": "Aureva Wellness API. POST to /api/contact."}
