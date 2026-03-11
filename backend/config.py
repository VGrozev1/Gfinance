"""Load configuration from environment."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from backend/ so it works regardless of run directory
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")  # Dashboard > Settings > API > JWT Secret

# Google Calendar
def _resolve_path(p: str) -> str:
    if not p:
        return ""
    path = Path(p)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    return str(path)

GOOGLE_SERVICE_ACCOUNT_FILE = _resolve_path(
    os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "credentials/google-calendar.json")
)
# For Vercel: JSON content as string (credentials file is gitignored)
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "")
GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "")

# Email (optional - if not set, logs instead of sending)
EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST", "")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
EMAIL_SMTP_USER = os.getenv("EMAIL_SMTP_USER", "")
EMAIL_SMTP_PASSWORD = os.getenv("EMAIL_SMTP_PASSWORD", "")

# API base URL for Confirm/Decline links in emails (e.g. http://localhost:8000)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Admin emails (comma-separated). Users with these emails get role=admin.
_ADMIN_EMAILS = os.getenv("ADMIN_EMAILS", "vikigrozev@gmail.com,bibigrozeva@gmail.com")
ADMIN_EMAILS = {e.strip().lower() for e in _ADMIN_EMAILS.split(",") if e.strip()}
