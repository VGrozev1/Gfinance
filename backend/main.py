import logging
import sys
from pathlib import Path
from urllib.parse import unquote, parse_qsl, urlencode

from typing import Optional
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("gfinance")
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .limiter import limiter

# Ensure backend is on path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

app = FastAPI(title="Gfinance Backend")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(GZipMiddleware, minimum_size=500)


class VercelPathMiddleware:
    """Restore path from X-Original-Path header (frontend) or x-path query (e.g. /confirm, /decline GET)."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return
        new_path = None
        from_header = False
        headers = list(scope.get("headers") or [])
        for k, v in headers:
            if k == b"x-original-path":
                raw = v.decode("utf-8", errors="replace").strip()
                if raw and raw.startswith("/"):
                    new_path = raw.rstrip("/") if len(raw) > 1 else raw
                    from_header = True
                break
        if not from_header:
            qs = scope.get("query_string", b"").decode("utf-8")
            for part in qs.split("&"):
                if part.startswith("x-path="):
                    raw = unquote(part[7:].strip())
                    if raw and raw.startswith("/"):
                        new_path = raw.rstrip("/") if len(raw) > 1 else raw
                        new_qs = urlencode([(k, v) for k, v in parse_qsl(qs, keep_blank_values=True) if k != "x-path"])
                        scope = dict(scope)
                        scope["path"] = new_path
                        scope["raw_path"] = new_path.encode("utf-8")
                        scope["query_string"] = new_qs.encode("utf-8")
                    break
        if from_header and new_path:
            scope = dict(scope)
            scope["path"] = new_path
            scope["raw_path"] = new_path.encode("utf-8")
            scope["headers"] = [(k, v) for k, v in headers if k != b"x-original-path"]
        await self.app(scope, receive, send)


app.add_middleware(VercelPathMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.booking import router as booking_router
from routes.auth import router as auth_router
from routes.booking import (
    BookRequest,
    _create_booking_with_auth,
    _get_email_from_auth as booking_get_email,
)
from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_booking_security = HTTPBearer(auto_error=False)


async def _vercel_book_post_impl(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials],
):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")
    body = {k: v for k, v in (body or {}).items() if k != "_path"}
    try:
        req = BookRequest(**body)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    auth_email = await booking_get_email(credentials)
    if not auth_email:
        raise HTTPException(status_code=401, detail="Моля влезте в профила си, за да направите запис.")
    return await _create_booking_with_auth(req, auth_email)


@app.post("/api")
@app.post("/api/")
async def vercel_book_post(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_booking_security),
):
    """Vercel: POST /api (or /api/) with JSON body so body is preserved."""
    return await _vercel_book_post_impl(request, credentials)


@app.on_event("startup")
async def startup():
    from config import EMAIL_SMTP_HOST, EMAIL_SMTP_USER
    logger.info("Gfinance backend starting")
    if EMAIL_SMTP_HOST and EMAIL_SMTP_USER:
        logger.info("Email configured: sending from %s via %s", EMAIL_SMTP_USER, EMAIL_SMTP_HOST)
    else:
        logger.warning("Email NOT configured. Appointment emails will not be sent. Set EMAIL_SMTP_* in backend/.env")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Gfinance backend shutting down")


app.include_router(booking_router)
app.include_router(auth_router)


@app.get("/health")
async def health_check() -> dict:
    """
    Simple health check endpoint used for monitoring and uptime checks.
    """
    return {"status": "ok"}


# Mount frontend last so /health and API routes take precedence
_frontend = Path(__file__).resolve().parent.parent / "frontend"
if _frontend.exists():
    app.mount("/", StaticFiles(directory=str(_frontend), html=True), name="frontend")


# To run locally (from project root):
# uvicorn main:app --reload

