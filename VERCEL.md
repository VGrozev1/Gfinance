# Deploying to Vercel

Static files (HTML, CSS, JS) are served from Vercel's CDN. The API runs as a Python serverless function. The build copies `frontend/` → `public/` for static serving.

## Quick deploy

1. Push your code to GitHub.
2. Go to [vercel.com/new](https://vercel.com/new) and import your repo.
3. Set environment variables (see below).
4. Deploy.

## Environment variables

Add these in **Vercel Dashboard → Project → Settings → Environment Variables**:

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_ANON_KEY` | Supabase anon key (also used by backend to fetch JWKS `/auth/v1/keys` for RS/ES JWT verification) |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key |
| `SUPABASE_JWT_SECRET` | **Required for booking.** Supabase JWT secret (Dashboard → Settings → API). Without it, logged-in users get "login required" when submitting a booking. |
| `GOOGLE_CALENDAR_ID` | Your Google Calendar ID (e.g. `you@gmail.com`) |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | **Full JSON content** of the service account key (one line). Paste the entire contents of `credentials/google-calendar.json`. |
| `API_BASE_URL` | Your Vercel URL, e.g. `https://your-project.vercel.app` |
| `EMAIL_SMTP_HOST` | e.g. `smtp.gmail.com` |
| `EMAIL_SMTP_PORT` | `587` |
| `EMAIL_SMTP_USER` | Your SMTP email |
| `EMAIL_SMTP_PASSWORD` | SMTP app password |
| `ADMIN_EMAILS` | Comma-separated admin emails |

## Google Calendar on Vercel

Because `credentials/` is gitignored, the JSON key file is not deployed. Use `GOOGLE_SERVICE_ACCOUNT_JSON` instead:

1. Open `backend/credentials/google-calendar.json`
2. Copy the entire JSON (minified, one line)
3. Paste as the value of `GOOGLE_SERVICE_ACCOUNT_JSON` in Vercel env vars

## After deploy

1. Set `API_BASE_URL` to your production URL so Confirm/Decline links in emails work.
2. Test booking and confirm flow.
