## Project Roadmap

High-level steps to turn your static HTML/CSS site into a working company website using JavaScript on the frontend and Python on the backend.

---

## 0. Your Manual Setup & Credentials Handoff

**Do these steps yourself** before we implement booking, auth, and email. After each setup, you’ll add the values to a `.env` file (never commit it). You can then share them with me in a secure way or paste them into `.env` locally; I will use them only as environment variables in code.

### 0.1 Supabase (Database & Auth)

**What you do:**

1. Go to [supabase.com](https://supabase.com) and create an account (or sign in).
2. Create a new project:
   - **Name:** e.g. `gfinance`
   - **Database password:** choose a strong password and **save it** (you’ll need it for the connection string).
   - **Region:** choose closest to your users.
3. Wait for the project to finish provisioning.
4. In the left sidebar: **Settings → API**.
5. Note down:
   - **Project URL**
   - **anon (public) key**
   - **service_role key** (keep this secret; used only by the backend).
6. In **Settings → Database**, copy the **Connection string** (URI) for "Session mode" or "Transaction mode". It looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
   Replace `[YOUR-PASSWORD]` with the database password you set.

**What to give me (or put in `backend/.env`):**

| Variable | Description | Example |
|----------|-------------|---------|
| `SUPABASE_URL` | Project URL | `https://xxxxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Public anon key | `eyJhbGc...` |
| `SUPABASE_SERVICE_ROLE_KEY` | Service role key (secret) | `eyJhbGc...` |
| `DATABASE_URL` | Full PostgreSQL connection string | `postgresql://postgres:xxx@db.xxx.supabase.co:5432/postgres` |

**Optional:** If you want Supabase Auth (instead of custom auth), we can switch Section 7 to use Supabase Auth and you’ll only need the anon key for the frontend; the backend can use the service role key for admin operations.

---

### 0.2 Google Calendar (Booking)

**What you do:**

1. Go to [Google Cloud Console](https://console.cloud.google.com).
2. Create a new project (or use an existing one):
   - **Project name:** e.g. `Gfinance`
3. Enable the **Google Calendar API**:
   - **APIs & Services → Library** → search "Google Calendar API" → **Enable**.
4. Create a **Service Account** (for a single company calendar):
   - **APIs & Services → Credentials → Create Credentials → Service Account**.
   - **Name:** e.g. `gfinance-calendar`
   - **Create and Continue** (skip optional steps).
5. Create a key for the service account:
   - Open the service account → **Keys** tab → **Add key → Create new key** → **JSON** → **Create**.
   - A JSON file downloads. **Keep it secure** and never commit it.
6. Share your company Google Calendar with the service account:
   - Open [Google Calendar](https://calendar.google.com).
   - Find the calendar you want bookings to go to → **Settings** → **Share with specific people**.
   - Add the service account email (e.g. `gfinance-calendar@your-project.iam.gserviceaccount.com`) with **Make changes to events** permission.
7. Get your **Calendar ID**:
   - In Calendar Settings, under **Integrate calendar**, copy the **Calendar ID** (often looks like `xxx@group.calendar.google.com` or your email).

**What to give me (or put in `backend/.env`):**

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path to the JSON key file, or the JSON content as a string | `./credentials/google-calendar.json` |
| `GOOGLE_CALENDAR_ID` | Calendar ID to create events in | `primary` or `xxx@group.calendar.google.com` |

**Alternative:** Put the JSON file in `backend/credentials/google-calendar.json` (add `credentials/` to `.gitignore`) and set `GOOGLE_SERVICE_ACCOUNT_FILE=credentials/google-calendar.json`.

---

### 0.3 Email (Confirmation after booking)

**What you do (choose one):**

**Option A – Gmail SMTP (simplest):**

1. Use a Gmail account.
2. Enable 2FA on that account.
3. Create an **App Password**: Google Account → Security → 2-Step Verification → App passwords → Generate for "Mail".
4. Note the 16-character app password.

**What to give me:** `EMAIL_SMTP_HOST`, `EMAIL_SMTP_PORT`, `EMAIL_SMTP_USER`, `EMAIL_APP_PASSWORD` (or `EMAIL_SMTP_PASSWORD`).

**Option B – SendGrid / Mailgun:**

1. Sign up at [sendgrid.com](https://sendgrid.com) or [mailgun.com](https://mailgun.com).
2. Create an API key (SendGrid) or get SMTP credentials (Mailgun).
3. Verify your sending domain or email.

**What to give me:** API key or SMTP credentials per the provider’s docs.

---

### 0.4 Checklist: What I Need From You

Before implementing Steps 5, 6, 7, I need:

- [x] **Supabase:** `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL` ✅ (in `backend/.env`)
  - Add `SUPABASE_JWT_SECRET` (Dashboard → Settings → API → JWT Secret) for backend JWT verification.
- [x] **Google Calendar:** `GOOGLE_SERVICE_ACCOUNT_FILE` and `GOOGLE_CALENDAR_ID` ✅
- [ ] **Email:** SMTP or API credentials (depending on your choice)
- [x] **Admin emails:** vikigrozev@gmail.com, bibigrozeva@gmail.com (in `ADMIN_EMAILS`; change in `.env` anytime)
- [ ] **(Before launch – don’t forget)** Consultant emails: replace placeholders with real consultant name → email mapping for booking notifications (Section 5)

**How to share:** Add these to `backend/.env` (I’ll create a `.env.example` template). Never commit `.env` to Git. For a secure handoff, use a password manager, encrypted message, or similar.

---

## 1. Clarify Requirements

- [x] **1.1 Content pages** ✅
  - Pages: `Home`, `About`, `Consultants`, `Credit Info`, `Credit Calculator`, `Booking`, `Booking Confirmed`, `My Profile`, `My Appointments`, `Login`, `Sign-up`.
  - Decide what should be editable in the future (texts, prices, contact info, etc.).
- **1.2 Booking**
  - **Choice: Google Calendar** for appointments. *(Easier alternative: Calendly or Cal.com — embed a link/widget, they handle availability and confirmation emails with zero backend work. Use Google Calendar if you need full control or to sync with an existing company calendar.)*
  - Decide what information is collected on booking (name, email, service, preferred time, notes).
- **1.3 Calculator**
  - Single page (`credit_calculator`) with a basic formula. Details to be finalized later. Can run in the browser if logic is non-sensitive.
- **1.4 Login / Sign-up**
  - **User types:** (a) **Clients** — basic sign-up option; (b) **Admins** — ~3–4 accounts, credentials to be provided later.
  - **Storage:** Use a **database** to store user info (clients and admins).
  - Custom auth in the backend (DB-backed), no third-party auth for now.

---

## 2. Frontend Structure (Static Pages) ✅

- [x] **File structure**
  - Create a basic structure like:
    - `index.html`, `about.html`, `services.html`, `contact.html`, etc.
    - `assets/css/` for styles.
    - `assets/js/` for scripts.
    - `assets/img/` for images/icons.
- [x] **Base layout**
  - Implement shared header, footer, navigation bar, and responsive layout.
  - Use a single main CSS file (`assets/css/main.css`) for site-wide styles.
  - Mobile-friendly (responsive design).
- [x] **Global JavaScript**
  - Add `assets/js/main.js` for:
    - Mobile menu behavior.
    - Smooth scrolling / small UI enhancements.
    - Shared helper functions (e.g. showing success/error messages).

---

## 3. Backend Tech Choice & Setup (Python) ✅

- **Chosen framework: FastAPI**
  - `fastapi` as the web framework.
  - `uvicorn[standard]` as the ASGI server for local/dev and production.
- **Project setup**
  - `backend/` folder created at the project root.
  - Inside `backend/`:
    - You should create and activate a Python virtual environment locally (e.g. `python -m venv .venv` then `source .venv/bin/activate` on macOS/Linux).
    - `requirements.txt` added with:
      - `fastapi`, `uvicorn[standard]` (server),
      - `sqlalchemy` (DB layer for later),
      - `python-dotenv` (env vars, to be wired with Pydantic settings later).
    - App entrypoint `main.py` created with a FastAPI instance.
  - Implemented endpoints:
    - `GET /health` → returns `{"status": "ok"}` for monitoring.
    - `GET /` → simple message `{"message": "Gfinance backend is running"}`.
  - Database setup (user tables for auth; see Section 7) will be added in a later step.

---

## 4. Frontend–Backend Integration Strategy ✅

- **Serving strategy (for development)**
  - FastAPI backend mounts the static `frontend/` directory at `/` using `StaticFiles`.
  - You can run everything with a single command from the project root:
    - `uvicorn backend.main:app --reload`
  - CORS is enabled with permissive settings during development to allow future JS `fetch` calls.
- **API design (high-level)**
  - Plan key endpoints:
    - `POST /api/book` – create a booking *request* (stored as pending); send email to consultant with Confirm/Decline links.
    - `POST /api/calc` – run the calculator with submitted data.
    - `POST /api/auth/signup` – register a user.
    - `POST /api/auth/login` – log in a user.
    - `POST /api/auth/logout` – log out a user (if using sessions).
    - `GET /api/auth/me` – return current user information (if authenticated).
- **Frontend usage**
  - A shared JS API client (`frontend/assets/js/api.js`) will be used by pages to call backend endpoints with `fetch`.
  - For now, it only defines base URL helpers and a `health` call; booking, calculator, and auth endpoints will be added in later steps.


## 5. Booking with Google Calendar + Email ✅

- **Flow: Request → Consultant approval → Calendar**
  1. **Client** submits a booking request (date, time, consultant, name, email, notes).
  2. Request is stored as **pending** in the database (e.g. Supabase `bookings` table).
  3. **Consultant** receives an email with the appointment details and **Confirm** / **Decline** buttons (links).
  4. **Confirm:** Backend creates the event in Google Calendar, updates the request to `confirmed`, and sends a confirmation email to the client.
  5. **Decline:** Backend updates the request to `declined` and optionally notifies the client.
- **Google Calendar setup**
  - Already configured (Section 0.2). Events are created only when the consultant confirms.
- **Backend integration**
  - `google_calendar.py`: Create events when consultant confirms.
  - `POST /api/book` – validate input, store pending request in DB, send email to **consultant** (not client yet).
  - `GET /api/book/confirm?token=xxx` (or `POST`) – consultant clicks Confirm link → create calendar event, notify client.
  - `GET /api/book/decline?token=xxx` – consultant clicks Decline link → update status, optionally notify client.
  - Each Confirm/Decline link includes a secure token (e.g. UUID) tied to the booking so only the consultant can act on it.
- **Database**
  - `bookings` table: `id`, `client_name`, `client_email`, `consultant_email`, `date`, `time`, `service`, `notes`, `status` (pending/confirmed/declined), `token`, `calendar_event_id` (after confirm), `created_at`.
- **Email**
  - **To consultant:** Appointment request details + Confirm button (link with token) + Decline button (link with token).
  - **To client (after confirm):** Confirmation with date, time, consultant.
  - **To client (after decline, optional):** “Your request could not be accommodated.”
- **Frontend booking form**
  - Fields: name, email, consultant (dropdown or select), preferred date, preferred time, service type, notes.
  - On submit: `POST /api/book` → show “Your request has been sent. The consultant will confirm shortly.”

---

## 6. Calculator Feature ✅

- **Define calculator specs**
  - Finalize formulas, required fields, and any constraints.
  - Decide:
    - **Frontend-only** (simple, non-sensitive logic), or
    - **Backend-based** (sensitive or complex calculations).
- **Frontend implementation**
  - Create a calculator section or page with the required input fields and a "Calculate" button.
  - If frontend-only:
    - Implement the calculation logic in `assets/js/calculator.js`.
    - On submit, prevent default and compute the result in the browser.
    - Display the result in the page (e.g. result box).
- **Backend-based calculator**
  - Implement `POST /api/calc`:
    - Validate inputs.
    - Run calculation logic in Python.
    - Return JSON with the computed result and any extra info.
  - In the frontend:
    - On submit, call `/api/calc` via `fetch`.
    - Show the result and handle error states.

---

## 7. Login / Sign-up (Authentication) ✅

- **Auth strategy:** **Supabase Auth** (not custom). Users sign up and log in via Supabase; the backend verifies JWTs.
- **User roles:** Clients (basic sign-up via Supabase) and Admins (~3–4 accounts, created in Supabase Dashboard or via a seed script).
- **Database:** Supabase PostgreSQL (credentials configured in `backend/.env`). Use Supabase Auth for identity; optional `profiles` or `user_roles` table for roles.
- **Supabase Auth flow**
  - **Frontend:** Use Supabase JS client (`@supabase/supabase-js`) on login/signup pages.
  - **Sign up:** `supabase.auth.signUp({ email, password })` → user receives confirmation email (if enabled).
  - **Login:** `supabase.auth.signInWithPassword({ email, password })` → returns session with JWT.
  - **Protected calls:** Send `Authorization: Bearer <access_token>` when calling backend; backend verifies JWT with Supabase.
  - **Logout:** `supabase.auth.signOut()`.
- **Backend**
  - Verify Supabase JWTs (using `SUPABASE_JWT_SECRET` from Dashboard or `service_role` key).
  - Optional: `GET /api/auth/me` that validates the token and returns user info.
  - Protect routes by requiring a valid JWT in the `Authorization` header.
- **Frontend auth UI**
  - Login and sign-up forms call Supabase Auth directly (no backend proxy needed for auth).
  - Store session in Supabase client (it handles localStorage/cookies).
  - Use `supabase.auth.onAuthStateChange()` to show/hide "Log out", protected links, etc.

---

## 8. Security and Performance Basics ✅

- **Security**
  - Validate and sanitize all user inputs (booking, calculator, auth).
  - Use HTTPS in all environments where real data is used.
  - Never store plain-text passwords.
  - Protect secrets (API keys, email credentials, Google credentials) with environment variables.
  - Consider rate limiting for auth and booking endpoints.
- **Performance**
  - Optimize and compress images and use modern formats where possible.
  - Use `defer` or `async` on script tags to avoid blocking page rendering.
  - Cache static assets aggressively via your hosting provider.
  - Keep JavaScript bundles small and split code into small modules as needed.

---

## 9. Configuration & Environments ✅

- **Environment variables**
  - Define and document required env vars, such as:
    - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_CALENDAR_ID`.
    - `EMAIL_SMTP_HOST`, `EMAIL_SMTP_USER`, `EMAIL_SMTP_PASSWORD`.
    - `JWT_SECRET_KEY` (if using custom JWT-based auth).
  - Use a `.env` file locally (never commit it) and platform-specific secret managers in production.
- **Environments**
  - Local development:
    - Run frontend (file server or simple dev server) and backend locally.
  - Staging (optional but recommended):
    - Deploy preview versions of frontend and backend for testing.
  - Production:
    - Deploy to live hosting and configure domain, SSL, and environment variables.

---

## 10. Deployment & Monitoring ✅

- **Frontend deployment**
  - Choose a static host (Netlify, Vercel, GitHub Pages, or similar).
  - Set up automatic builds from your repository if using Git.
- **Backend deployment**
  - Deploy Python backend to a service that supports FastAPI/Flask apps (Render, Railway, Fly.io, etc. or your own VPS).
  - Configure:
    - Environment variables.
    - HTTPS (either directly or via a reverse proxy).
    - A process manager (if on a VPS) such as `gunicorn` + `uvicorn` workers for FastAPI.
- **Monitoring and logging**
  - Implement structured logging in the backend (request logs, error logs).
  - Add uptime monitoring (e.g. a simple external monitor that hits `/health`).
  - Add basic analytics on the frontend (Plausible, Matomo, or Google Analytics) to understand usage.

---

## 11. Next Steps (Implementation Order)

1. ~~Finalize page list and features (Section 1).~~ ✅
2. ~~Build static HTML/CSS layout and global JS (Section 2).~~ ✅
3. ~~Set up Python backend (Section 3).~~ ✅
4. ~~Frontend–backend integration (Section 4).~~ ✅
5. **→ Do Section 0 first** (your manual setup: Supabase, Google Calendar, email credentials).
6. Implement the booking flow (Section 5).
7. Implement the calculator (frontend or backend) and its UI (Section 6).
8. Add login/sign-up flows (Section 7).
9. ~~Tighten security and performance (Section 8).~~ ✅
10. ~~Set up configuration and environments (Section 9).~~ ✅
11. ~~Deploy and add monitoring (Section 10).~~ ✅
