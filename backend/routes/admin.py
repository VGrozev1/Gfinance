"""Admin API routes — all-bookings dashboard."""
import jwt
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from config import ADMIN_EMAILS
from jwt_utils import decode_supabase_jwt
from limiter import limiter

router = APIRouter(prefix="/api/admin", tags=["admin"])
security = HTTPBearer(auto_error=False)

_ALLOWED_STATUSES = {"pending", "confirmed", "declined", "cancelled"}


async def _require_admin(credentials: Optional[HTTPAuthorizationCredentials]) -> str:
    if not credentials:
        raise HTTPException(status_code=401, detail="Моля влезте в профила си.")
    try:
        payload = decode_supabase_jwt(credentials.credentials)
        email = (payload.get("email") or "").lower()
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Сесията е изтекла. Влезте отново.")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Невалиден токен: {e}")
    if email not in ADMIN_EMAILS:
        raise HTTPException(status_code=403, detail="Нямате администраторски достъп.")
    return email


class StatusUpdate(BaseModel):
    status: str


@router.get("/bookings")
@limiter.limit("60/minute")
async def list_all_bookings(
    request: Request,
    status: Optional[str] = None,
    consultant_id: Optional[str] = None,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """Return all bookings for admin view. Optionally filter by status and/or consultant_id."""
    await _require_admin(credentials)
    from routes.booking import get_supabase
    supabase = get_supabase()
    q = supabase.table("bookings").select(
        "id, client_name, client_email, consultant_id, booking_date, booking_time, service, notes, status, created_at"
    )
    if status and status in _ALLOWED_STATUSES:
        q = q.eq("status", status)
    if consultant_id:
        q = q.eq("consultant_id", consultant_id)
    r = q.order("booking_date", desc=True).order("booking_time", desc=True).execute()
    return {"bookings": r.data or []}


@router.patch("/bookings/{booking_id}")
@limiter.limit("30/minute")
async def update_booking_status(
    request: Request,
    booking_id: str,
    body: StatusUpdate,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """Update a booking's status. Admin only."""
    await _require_admin(credentials)
    if body.status not in _ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail=f"Невалиден статус: {body.status}")
    from routes.booking import get_supabase
    supabase = get_supabase()
    r = supabase.table("bookings").select("id, status").eq("id", booking_id).execute()
    if not r.data:
        raise HTTPException(status_code=404, detail="Заявката не е намерена.")
    supabase.table("bookings").update({"status": body.status}).eq("id", booking_id).execute()
    return {"ok": True}
