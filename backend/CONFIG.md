# Gfinance – Configuration & Environments

This document describes how to configure the Gfinance backend for local development, staging, and production.

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in the values. **Never commit `.env` to Git.**

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Supabase project URL |
| `SUPABASE_ANON_KEY` | Yes | Supabase public anon key (frontend uses via supabase-config.js) |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Supabase service role key (backend only; keep secret) |
| `SUPABASE_JWT_SECRET` | Yes | JWT secret from Supabase Dashboard → Settings → API |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Yes | Path to Google service account JSON (e.g. `credentials/google-calendar.json`) |
| `GOOGLE_CALENDAR_ID` | Yes | Calendar ID for booking events |
| `ADMIN_EMAILS` | Yes | Comma-separated admin emails |
| `API_BASE_URL` | Yes | Base URL for email links (e.g. `https://yourdomain.com`) |
| `EMAIL_SMTP_HOST` | No | SMTP host (if empty, emails are logged to console) |
| `EMAIL_SMTP_PORT` | No | SMTP port (default 587) |
| `EMAIL_SMTP_USER` | No | SMTP username |
| `EMAIL_SMTP_PASSWORD` | No | SMTP password / app password |

---

## Local Development

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   # or: .venv\Scripts\activate   # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in values.

4. Run the backend:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Open http://localhost:8000/ — the frontend is served from the same process.

---

## Staging (Optional)

- Deploy to a preview environment (e.g. Render preview, Railway preview).
- Set `API_BASE_URL` to the staging URL.
- Use the same `.env` variables; consider separate Supabase/Google projects for staging if needed.

---

## Production

1. **Environment variables**  
   Set all required variables in your hosting platform’s secret manager (Render, Railway, Fly.io, VPS, etc.). Do not use `.env` files in production.

2. **HTTPS**  
   Use HTTPS for the app. Most platforms provide SSL; otherwise use a reverse proxy (nginx, Caddy) with Let’s Encrypt.

3. **API_BASE_URL**  
   Set to your production URL (e.g. `https://app.gfinance.bg`). It is used in booking confirmation/decline links in emails.

4. **Run command**  
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```
   For more traffic, use multiple workers:
   ```bash
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

5. **Frontend**  
   Update `frontend/assets/js/supabase-config.js` or use `data-api-base` so the frontend points to your production API URL.
