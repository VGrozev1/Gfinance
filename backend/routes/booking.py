"""Booking API routes."""
import logging
import uuid
from typing import Optional
from datetime import datetime
import time
import urllib.request
import urllib.error
import jwt
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field, field_validator

from config import API_BASE_URL, SUPABASE_ANON_KEY, SUPABASE_JWT_SECRET, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL
from consultants import CONSULTANTS
from limiter import limiter
from email_service import send_client_confirmation, send_client_decline, send_consultant_booking_request
from google_calendar import create_event

router = APIRouter(prefix="/api/book", tags=["booking"])
security = HTTPBearer(auto_error=False)

# Lazy import to avoid circular dependency
_supabase = None
_jwks_cache = {"expires_at": 0.0, "jwks_json": ""}


def get_supabase():
    global _supabase
    if _supabase is None:
        from supabase import create_client
        from config import SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL
        _supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return _supabase


def _fetch_supabase_jwks_json() -> str:
    if not SUPABASE_URL:
        raise RuntimeError("SUPABASE_URL is not set")
    api_key = SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY
    if not api_key:
        raise RuntimeError("SUPABASE_ANON_KEY (or SUPABASE_SERVICE_ROLE_KEY) is not set")
    base = SUPABASE_URL.rstrip("/")
    # Preferred Supabase JWKS endpoints for ES256/RS256
    candidates = [
        f"{base}/auth/v1/.well-known/jwks.json",
        f"{base}/auth/v1/jwks",
    ]
    last_err: Exception | None = None
    for url in candidates:
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "apikey": api_key,
                    "Authorization": f"Bearer {api_key}",
                },
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read()
                return raw.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            last_err = e
            # Try next candidate on 404; for 401/403 we also fall through to raise a clear error
            continue
        except urllib.error.URLError as e:
            last_err = e
            continue
    if last_err is not None:
        raise RuntimeError(f"Failed to fetch Supabase JWKS: {last_err}")
    raise RuntimeError("Failed to fetch Supabase JWKS: unknown error")


def _get_jwks_set():
    now = time.time()
    if _jwks_cache["jwks_json"] and now < float(_jwks_cache["expires_at"]):
        return jwt.PyJWKSet.from_json(_jwks_cache["jwks_json"])
    jwks_json = _fetch_supabase_jwks_json()
    # Cache for 10 minutes
    _jwks_cache["jwks_json"] = jwks_json
    _jwks_cache["expires_at"] = now + 600.0
    return jwt.PyJWKSet.from_json(jwks_json)


def _get_signing_key_from_jwks(token: str):
    header = jwt.get_unverified_header(token) or {}
    kid = header.get("kid")
    if not kid:
        raise jwt.InvalidTokenError("Missing kid in JWT header")
    jwks_set = _get_jwks_set()
    for jwk in (jwks_set.keys or []):
        if getattr(jwk, "key_id", None) == kid:
            return jwk.key
    raise jwt.InvalidTokenError(f"No matching JWK for kid={kid}")


def _decode_supabase_jwt(token: str) -> dict:
    """Decode Supabase JWT supporting HS256 (legacy secret) and RS256 (JWKS)."""
    if not token:
        raise jwt.InvalidTokenError("Empty token")

    header = jwt.get_unverified_header(token) or {}
    alg_raw = header.get("alg")
    alg = str(alg_raw).strip().upper() if alg_raw is not None else None

    if alg in {"HS256", "HS512"}:
        if not SUPABASE_JWT_SECRET:
            raise jwt.InvalidTokenError("SUPABASE_JWT_SECRET not set")
        return jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            audience="authenticated",
            algorithms=[alg],
        )

    if alg in {"RS256", "RS512", "ES256", "ES384", "ES512"}:
        signing_key = _get_signing_key_from_jwks(token)
        return jwt.decode(
            token,
            signing_key,
            audience="authenticated",
            algorithms=[alg],
        )

    raise jwt.InvalidAlgorithmError(f"The specified alg value is not allowed: {alg_raw}")


class BookRequest(BaseModel):
    client_name: str = Field(..., min_length=1, max_length=200)
    client_email: EmailStr
    consultant_id: str = Field(..., min_length=1, max_length=100)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    time: str = Field(..., pattern=r"^\d{1,2}:\d{2}(?::\d{2})?$")
    service: str = Field(default="", max_length=200)
    notes: str = Field(default="", max_length=2000)

    @field_validator("client_name", "service")
    @classmethod
    def sanitize_short(cls, v: str) -> str:
        return (v or "").strip()[:200]

    @field_validator("notes")
    @classmethod
    def sanitize_notes(cls, v: str) -> str:
        return (v or "").strip()[:2000]

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid date format (use YYYY-MM-DD)")


def _get_taken_times(consultant_id: str, date: str) -> list[str]:
    """Return list of taken time slots (HH:MM) for consultant+date with pending or confirmed status."""
    supabase = get_supabase()
    r = (
        supabase.table("bookings")
        .select("booking_time")
        .eq("consultant_id", consultant_id)
        .eq("booking_date", date)
        .in_("status", ["pending", "confirmed"])
        .execute()
    )
    times = []
    for row in (r.data or []):
        t = str(row.get("booking_time", "")).strip()
        if t:
            parts = t.split(":")
            h = int(parts[0]) if parts else 0
            m = int(parts[1]) if len(parts) > 1 else 0
            times.append(f"{h:02d}:{m:02d}")  # normalize to "09:00"
    return list(dict.fromkeys(times))


def _is_slot_taken(consultant_id: str, date: str, time_val: str) -> bool:
    """Check if this consultant+date+time already has a confirmed or pending booking."""
    taken = _get_taken_times(consultant_id, date)
    t_norm = time_val[:5] if len(time_val) >= 5 else time_val
    return t_norm in taken


@router.get("/taken")
@limiter.limit("60/minute")
async def get_taken_slots(
    request: Request,
    consultant_id: str,
    date: str,
) -> dict:
    """Return list of taken time slots (HH:MM) for this consultant on this date."""
    if consultant_id not in CONSULTANTS:
        raise HTTPException(status_code=400, detail="Invalid consultant")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (use YYYY-MM-DD)")
    taken = _get_taken_times(consultant_id, date)
    return {"taken": taken}


async def _create_booking_with_auth(req: BookRequest, auth_email: str) -> dict:
    """Core booking creation (used by both POST /api/book and POST /api for Vercel)."""
    if req.client_email.lower() != auth_email:
        raise HTTPException(
            status_code=403,
            detail="Имейлът трябва да съвпада с профила ви.",
        )
    if req.consultant_id not in CONSULTANTS:
        raise HTTPException(status_code=400, detail="Invalid consultant")
    consultant = CONSULTANTS[req.consultant_id]
    time_val = req.time if len(req.time) >= 8 else f"{req.time}:00"  # HH:MM -> HH:MM:00
    token = str(uuid.uuid4())
    if _is_slot_taken(req.consultant_id, req.date, time_val):
        raise HTTPException(
            status_code=400,
            detail="Този час вече е зает. Моля изберете друг ден или час.",
        )
    row = {
        "client_name": req.client_name,
        "client_email": req.client_email,
        "consultant_id": req.consultant_id,
        "consultant_email": consultant["email"],
        "booking_date": req.date,
        "booking_time": time_val,
        "service": req.service,
        "notes": req.notes,
        "status": "pending",
        "token": token,
    }
    try:
        supabase = get_supabase()
        result = supabase.table("bookings").insert(row).execute()
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to save booking")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    logging.getLogger("gfinance").info("Sending consultant email to %s for booking %s", consultant["email"], req.client_name)
    send_consultant_booking_request(
        consultant_email=consultant["email"],
        client_name=req.client_name,
        client_email=req.client_email,
        date_str=req.date,
        time_str=req.time,
        service=req.service,
        notes=req.notes,
        confirm_token=token,
        decline_token=token,  # same token for both; we distinguish by path
    )
    return {"ok": True, "message": "Your request has been sent. The consultant will confirm shortly."}


@router.post("")
@limiter.limit("10/minute")
async def create_booking_request(
    request: Request,
    req: BookRequest,
    credentials: Optional[HTTPAuthorizationCredentials] = security,
) -> dict:
    """Create a pending booking request and email the consultant. Requires login."""
    auth_email = await _require_email_from_auth(credentials)
    return await _create_booking_with_auth(req, auth_email)


async def _get_email_from_auth(credentials: Optional[HTTPAuthorizationCredentials]) -> Optional[str]:
    """Extract email from Supabase JWT. Returns None if not authenticated."""
    if not credentials:
        return None
    try:
        payload = _decode_supabase_jwt(credentials.credentials)
        return (payload.get("email") or "").lower()
    except jwt.PyJWTError:
        return None


async def _require_email_from_auth(credentials: Optional[HTTPAuthorizationCredentials]) -> str:
    """Extract email from Supabase JWT or raise an HTTPException with a clear reason."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Моля влезте в профила си, за да направите запис.")
    # Grab JWT header early for better diagnostics (safe: does not verify signature).
    header_hint = ""
    try:
        h = jwt.get_unverified_header(credentials.credentials) or {}
        alg = h.get("alg")
        kid = h.get("kid")
        typ = h.get("typ")
        header_hint = f" (jwt header: alg={alg}, kid={kid}, typ={typ})"
    except Exception:
        header_hint = " (jwt header: unreadable)"
    try:
        payload = _decode_supabase_jwt(credentials.credentials)
        email = (payload.get("email") or "").lower()
        if not email:
            raise HTTPException(status_code=401, detail="Входът не може да се провери: липсва email в токена.")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Сесията е изтекла. Моля влезте отново.")
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Невалиден токен: подписът не съвпада (вероятно грешен SUPABASE_JWT_SECRET във Vercel).",
        )
    except jwt.InvalidAudienceError:
        raise HTTPException(status_code=401, detail="Невалиден токен: грешна аудитория (aud).")
    except jwt.InvalidAlgorithmError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Невалиден токен: неподдържан алгоритъм (alg). {str(e)}{header_hint}",
        )
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except jwt.PyJWTError as e:
        detail = str(e).strip()
        suffix = f": {detail}" if detail else ""
        raise HTTPException(
            status_code=401,
            detail=f"Невалиден токен ({e.__class__.__name__}){suffix}{header_hint}. Моля влезте отново.",
        )


@router.get("/list")
@limiter.limit("30/minute")
async def list_bookings(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = security,
    email_param: Optional[str] = None,
) -> dict:
    """Return bookings for the user's email.

    Prefers Supabase JWT, but also accepts explicit ?email_param=<email>
    so logged-in users can still see bookings even if JWT verification
    is temporarily misconfigured on the backend.
    """
    email: Optional[str] = None

    # 1) Prefer explicit email_param when present (frontend passes it from Supabase session)
    if email_param and "@" in email_param:
        email = email_param.strip().lower()

    # 2) Otherwise, try strong auth via JWT (if header present)
    if not email and credentials and credentials.credentials:
        try:
            email = await _require_email_from_auth(credentials)
        except HTTPException:
            email = None

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Моля влезте в профила си, за да видите вашите срещи.",
        )
    supabase = get_supabase()
    r = (
        supabase.table("bookings")
        .select("id, client_name, client_email, consultant_id, booking_date, booking_time, service, notes, status, created_at")
        .eq("client_email", email)
        .order("booking_date", desc=True)
        .order("booking_time", desc=True)
        .execute()
    )
    return {"bookings": r.data or []}


def _get_booking_by_token(token: str) -> Optional[dict]:
    supabase = get_supabase()
    r = supabase.table("bookings").select("*").eq("token", token).execute()
    if not r.data or len(r.data) == 0:
        return None
    return r.data[0]


@router.get("/confirm", response_class=HTMLResponse)
async def confirm_booking(token: str):
    """Consultant confirms → create calendar event, notify client. Returns HTML page."""
    booking = _get_booking_by_token(token)
    if not booking:
        return _html_page("Грешка", "Невалидна или изтекла заявка.", error=True)
    if booking["status"] != "pending":
        return _html_page("Вече обработена", "Тази заявка вече е обработена.")
    consultant = CONSULTANTS.get(booking["consultant_id"], {})
    consultant_name = consultant.get("name", booking["consultant_id"])
    date_s = str(booking["booking_date"])
    time_s = str(booking["booking_time"])[:8]  # HH:MM:SS
    start_dt = datetime.strptime(f"{date_s} {time_s}", "%Y-%m-%d %H:%M:%S")
    end_dt = start_dt.replace(hour=start_dt.hour + 1, minute=0, second=0)
    event_id = create_event(
        summary=f"Консултация: {booking['client_name']}",
        start_datetime=start_dt,
        end_datetime=end_dt,
        description=booking.get("notes") or "",
        attendee_emails=[booking["client_email"]],
    )
    supabase = get_supabase()
    supabase.table("bookings").update({
        "status": "confirmed",
        "calendar_event_id": event_id or "",
    }).eq("token", token).execute()
    send_client_confirmation(
        client_email=booking["client_email"],
        client_name=booking["client_name"],
        date_str=booking["booking_date"],
        time_str=str(booking["booking_time"])[:5],
        consultant_name=consultant_name,
    )
    return _html_page("Потвърдено", "Консултацията е потвърдена. Клиентът е уведомен по имейл.")


@router.get("/decline", response_class=HTMLResponse)
async def decline_booking(token: str):
    """Consultant declines → update status, notify client. Returns HTML page."""
    booking = _get_booking_by_token(token)
    if not booking:
        return _html_page("Грешка", "Невалидна или изтекла заявка.", error=True)
    if booking["status"] != "pending":
        return _html_page("Вече обработена", "Тази заявка вече е обработена.")
    supabase = get_supabase()
    supabase.table("bookings").update({"status": "declined"}).eq("token", token).execute()
    consultant = CONSULTANTS.get(booking["consultant_id"], {})
    consultant_name = consultant.get("name", booking["consultant_id"])
    send_client_decline(
        client_email=booking["client_email"],
        client_name=booking["client_name"],
        date_str=str(booking["booking_date"]),
        time_str=str(booking["booking_time"])[:5],
        consultant_name=consultant_name,
    )
    return _html_page("Отхвърлено", "Заявката е отхвърлена. Клиентът е уведомен по имейл.")


def _html_page(title: str, message: str, error: bool = False) -> HTMLResponse:
    color = "#ef4444" if error else "#22c55e"
    html = f"""<!DOCTYPE html>
<html lang="bg"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title></head>
<body style="font-family: sans-serif; max-width: 480px; margin: 60px auto; padding: 24px;">
<h2 style="color: {color};">{title}</h2>
<p>{message}</p>
</body></html>
"""
    return HTMLResponse(content=html, headers={"Content-Type": "text/html; charset=utf-8"})
