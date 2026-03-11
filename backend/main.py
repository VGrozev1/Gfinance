import logging
import sys
from pathlib import Path

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.booking import router as booking_router
from routes.auth import router as auth_router


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

