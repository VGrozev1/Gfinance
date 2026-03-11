## Backend / Server env vars (FastAPI / Vercel API)

Set these in Vercel **Environment Variables** for the backend runtime (serverless functions):

- **SUPABASE_URL**  
  - Value: `https://olbmqwmnawnwbrdodmcz.supabase.co`

- **SUPABASE_ANON_KEY**  
  - Value:  
    `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sYm1xd21uYXdud2JyZG9kbWN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMxNzA3NTcsImV4cCI6MjA4ODc0Njc1N30.hVFvwnZB2Lp7Q2aKZcW9CRDpo0Tr1XCVj9v8-zPTJrQ`

- **SUPABASE_SERVICE_ROLE_KEY**  
  - Value:  
    `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sYm1xd21uYXdud2JyZG9kbWN6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MzE3MDc1NywiZXhwIjoyMDg4NzQ2NzU3fQ.znGXCOE1XsSZ3_4iLp3l7aSbJUZavBsCXA2ayBDjr_Y`

- **DATABASE_URL**  
  - Value:  
    `postgresql://postgres:1DgvyWZZruK0Ze7m@db.olbmqwmnawnwbrdodmcz.supabase.co:5432/postgres`

- **GOOGLE_SERVICE_ACCOUNT_FILE**  
  - For local only (file path). On Vercel you instead use `GOOGLE_SERVICE_ACCOUNT_JSON`.  
  - Local value: `credentials/google-calendar.json`

- **GOOGLE_SERVICE_ACCOUNT_JSON**  
  - For Vercel: paste the **full JSON** content of `backend/credentials/google-calendar.json` as a single-line string.

- **GOOGLE_CALENDAR_ID**  
  - Value: `vikigrozev@gmail.com`

- **ADMIN_EMAILS**  
  - Value: `vikigrozev@gmail.com,bibigrozeva@gmail.com`

- **SUPABASE_JWT_SECRET**  
  - Value: **“Legacy JWT secret (still used)”** from Supabase:  
    Supabase Dashboard → Project Settings → **API** → section “JWT Settings”.

- **API_BASE_URL**  
  - Local value in `.env`: `http://localhost:8000`  
  - For production emails (confirm/decline links) you probably want:  
    `https://<your-vercel-domain>`

- **EMAIL_SMTP_HOST**  
  - Value: `smtp.gmail.com`

- **EMAIL_SMTP_PORT**  
  - Value: `587`

- **EMAIL_SMTP_USER**  
  - Value: `foodydeliveryapp@gmail.com`

- **EMAIL_SMTP_PASSWORD**  
  - Value: `iyvtvsjalzhnyadd`

> To check Vercel: every name above should exist there with **exactly** the same value (except `API_BASE_URL`, which can differ between local and prod, and `GOOGLE_SERVICE_ACCOUNT_FILE`, which is local-only).

---

## Frontend (client-side) Supabase config

These are **hardcoded** in `frontend/assets/js/supabase-config.js` and must match the Supabase project:

- **window.SUPABASE_URL**  
  - Value: `https://olbmqwmnawnwbrdodmcz.supabase.co`

- **window.SUPABASE_ANON_KEY**  
  - Value:  
    `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sYm1xd21uYXdud2JyZG9kbWN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMxNzA3NTcsImV4cCI6MjA4ODc0Njc1N30.hVFvwnZB2Lp7Q2aKZcW9CRDpo0Tr1XCVj9v8-zPTJrQ`

