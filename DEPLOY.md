# Gfinance – Deployment & Monitoring

## Frontend Deployment

The frontend is static HTML/CSS/JS. You can deploy it in two ways:

### Option A: Same origin as backend (recommended for this setup)

The FastAPI backend serves the `frontend/` directory at `/`. Deploy the backend and the frontend is included. No separate frontend deployment needed.

### Option B: Separate static host

If you want the frontend on a CDN (Netlify, Vercel, GitHub Pages):

1. Deploy the `frontend/` folder as a static site.
2. Set the build output directory to `frontend` (or copy its contents to the publish dir).
3. Set **environment variable** or **build-time** `API_BASE_URL` to your backend URL (e.g. `https://api.gfinance.bg`).
4. Ensure `frontend/assets/js/supabase-config.js` and `api.js` use the correct API base for fetch calls.
5. Configure redirects so client-side routing works (e.g. `/* /index.html` for SPA-like behavior if needed).

---

## Backend Deployment

1. **Choose a host**: Render, Railway, Fly.io, or a VPS (DigitalOcean, etc.).

2. **Set environment variables** (see `backend/CONFIG.md` for the full list):
   - `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET`
   - `GOOGLE_SERVICE_ACCOUNT_FILE` (path or JSON content)
   - `GOOGLE_CALENDAR_ID`
   - `ADMIN_EMAILS`
   - `API_BASE_URL` (your production URL)
   - `EMAIL_SMTP_*` (for real emails)

3. **Run command**:
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```
   For higher traffic:
   ```bash
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

4. **HTTPS**: Enable SSL on your platform or use nginx/Caddy as a reverse proxy with Let’s Encrypt.

---

## Monitoring

### Uptime / Health checks

- **Endpoint**: `GET /health` → returns `{"status":"ok"}`
- Use an external service (UptimeRobot, Pingdom, Better Uptime) to call this URL every few minutes.
- Alert on non-2xx or timeouts.

### Backend logging

The backend uses Python `logging`:

- **Level**: INFO
- **Format**: `%(asctime)s [%(levelname)s] %(name)s: %(message)s`
- **Where**: stdout (view logs in your hosting dashboard: Render, Railway, etc.)

Example log line:
```
2025-03-10 14:30:00 [INFO] gfinance: Gfinance backend starting
```

### Frontend analytics (optional)

Add privacy-friendly analytics if needed:

- **Plausible**: add their script to `index.html` and other pages
- **Google Analytics**: add gtag.js
- **Matomo**: self-hosted option

Place the analytics script in the `<head>` of shared layouts or `index.html`.
