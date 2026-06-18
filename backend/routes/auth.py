"""Auth API routes - JWT verification and user info."""
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import ADMIN_EMAILS
from jwt_utils import decode_supabase_jwt
from limiter import limiter

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


async def _get_user_from_token(credentials: Optional[HTTPAuthorizationCredentials]) -> dict:
    """Verify Supabase JWT and return user payload. Raises HTTPException on invalid."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing authorization")
    try:
        payload = decode_supabase_jwt(credentials.credentials)
        email = (payload.get("email") or "").lower()
        role = "admin" if email in ADMIN_EMAILS else "client"
        return {"email": email, "role": role, "sub": payload.get("sub")}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/me")
@limiter.limit("30/minute")
async def get_me(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
):
    """Return current user info if valid JWT provided."""
    user = await _get_user_from_token(credentials)
    return {"email": user["email"], "role": user["role"]}
