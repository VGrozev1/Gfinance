"""Shared JWT utilities for Supabase token validation (HS256 and RS256/ES256)."""
import time
import urllib.error
import urllib.request

import jwt

from config import SUPABASE_ANON_KEY, SUPABASE_JWT_SECRET, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL

_jwks_cache: dict = {"expires_at": 0.0, "jwks_json": ""}


def _fetch_supabase_jwks_json() -> str:
    if not SUPABASE_URL:
        raise RuntimeError("SUPABASE_URL is not set")
    api_key = SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY
    if not api_key:
        raise RuntimeError("SUPABASE_ANON_KEY (or SUPABASE_SERVICE_ROLE_KEY) is not set")
    base = SUPABASE_URL.rstrip("/")
    candidates = [
        f"{base}/auth/v1/.well-known/jwks.json",
        f"{base}/auth/v1/jwks",
    ]
    last_err: Exception | None = None
    for url in candidates:
        try:
            req = urllib.request.Request(
                url,
                headers={"apikey": api_key, "Authorization": f"Bearer {api_key}"},
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            last_err = e
            continue
    raise RuntimeError(f"Failed to fetch Supabase JWKS: {last_err or 'unknown error'}")


def _get_jwks_set():
    now = time.time()
    if _jwks_cache["jwks_json"] and now < float(_jwks_cache["expires_at"]):
        return jwt.PyJWKSet.from_json(_jwks_cache["jwks_json"])
    jwks_json = _fetch_supabase_jwks_json()
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


def decode_supabase_jwt(token: str) -> dict:
    """Decode a Supabase JWT. Supports HS256/HS512 (secret) and RS256/ES256 (JWKS)."""
    if not token:
        raise jwt.InvalidTokenError("Empty token")

    header = jwt.get_unverified_header(token) or {}
    alg_raw = header.get("alg")
    alg = str(alg_raw).strip().upper() if alg_raw is not None else None

    if alg in {"HS256", "HS512"}:
        if not SUPABASE_JWT_SECRET:
            raise jwt.InvalidTokenError("SUPABASE_JWT_SECRET not set")
        return jwt.decode(token, SUPABASE_JWT_SECRET, audience="authenticated", algorithms=[alg])

    if alg in {"RS256", "RS512", "ES256", "ES384", "ES512"}:
        signing_key = _get_signing_key_from_jwks(token)
        return jwt.decode(token, signing_key, audience="authenticated", algorithms=[alg])

    raise jwt.InvalidAlgorithmError(f"The specified alg value is not allowed: {alg_raw}")
