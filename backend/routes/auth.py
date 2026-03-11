"""Auth API routes - JWT verification and user info."""
from typing import Optional

import jwt
from fastapi import APIRouter, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import ADMIN_EMAILS, SUPABASE_JWT_SECRET
from limiter import limiter

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


async def _get_user_from_token(credentials: Optional[HTTPAuthorizationCredentials]) -> dict:
    """Verify Supabase JWT and return user payload. Raises HTTPException on invalid."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing authorization")
    token = credentials.credentials
    if not SUPABASE_JWT_SECRET:
        raise HTTPException(status_code=500, detail="Auth not configured")
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            audience="authenticated",
            algorithms=["HS256"],
        )
        email = (payload.get("email") or "").lower()
        role = "admin" if email in ADMIN_EMAILS else "client"
        return {"email": email, "role": role, "sub": payload.get("sub")}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/me")
@limiter.limit("30/minute")
async def get_me(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = security,
):
    """Return current user info if valid JWT provided."""
    user = await _get_user_from_token(credentials)
    return {"email": user["email"], "role": user["role"]}
