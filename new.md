# Gfinance – Improvement List

## Security

1. ✅ **`email_param` auth bypass on `/api/book/list`**
   Anyone who knows a user's email can hit `/api/book/list?email_param=victim@email.com` with no token and see all of their bookings. Remove the `email_param` fallback entirely and require a valid JWT in all cases.

2. ✅ **CORS is wide-open (`allow_origins=["*"]`)**
   Lock it to your actual Vercel domain (e.g. `["https://gfinance.vercel.app"]`) in `backend/main.py`. Now controlled by the `CORS_ORIGINS` env var — set it in Vercel to your production URL. Defaults to `["*"]` only when the env var is not set (local dev).

3. ✅ **`routes/auth.py` only accepts HS256 tokens**
   The booking route has a full JWKS-based decoder supporting RS256/ES256. `auth.py`'s `_get_user_from_token` still only does `algorithms=["HS256"]`, so it will silently reject sessions if Supabase ever rotates to an asymmetric key. Extracted shared decoder to `backend/jwt_utils.py`; both `auth.py` and `booking.py` now import from there.

4. ✅ **Booking slot race condition (Python side)**
   `_is_slot_taken` and `supabase.table("bookings").insert(row)` are two separate DB calls with no transaction between them. Two users booking the same slot at the same millisecond will both pass the check and both get inserted. The insert now catches duplicate/unique constraint errors and returns a clean 400. **Still needed:** add a `UNIQUE (consultant_id, booking_date, booking_time)` constraint in the Supabase table editor to fully close this at the DB level.

---

## Performance

5. ✅ **Tailwind CDN in production**
   Every page loads the full Tailwind CDN script with JIT compilation in the browser. Replaced with a pre-built, purged CSS file (`tailwind.min.css`, 36KB vs ~350KB CDN). All 12 pages updated. Vercel build command updated to run `npx tailwindcss --minify` before copying files. Run `npm run build:css` locally after adding new HTML classes.

6. ✅ **Google Fonts loaded twice on several pages**
   `booking_confirmed`, `my_appointments`, and others had two `<link>` tags for `Material+Symbols+Outlined` (one without FILL, one with FILL). Removed the old one without the FILL axis from all 5 affected pages.

7. ✅ **SMTP connection opened per email**
   `email_service.py` opens and tears down a new SMTP connection for every email sent. This was blocking the booking API response for ~300–500 ms. Email is now sent via FastAPI `BackgroundTasks` — the HTTP response returns immediately after the DB insert, and the email fires in the background.

---

## Frontend / UX

8. **External stock images from `lh3.googleusercontent.com/aida-public`** *(partially done — booking_confirmed now uses local photos)*
   `credit_info`, `consultants_info`, `index.html`, `my_profile`, and `booking_confirmed` all use Google-hosted placeholder images. These can break, load slowly, or get blocked. Replace with owned images stored in `frontend/assets/images/`.

9. ✅ **No favicon**
   No page defines a `<link rel="icon">`. The browser tab shows a blank icon. Add a favicon at `frontend/assets/images/favicon.ico` and reference it in every page's `<head>`.

10. ✅ **No Open Graph / meta description tags**
    None of the pages have `<meta name="description">`, `og:title`, `og:image`, or `og:description` tags. This hurts SEO and looks bad when shared on social media.

11. ✅ **`booking_confirmed` is still phone-app width**
    The root container uses `max-w-md mx-auto` — the same narrow phone-app constraint that was fixed on `credit_calculator`. On desktop it looks like a narrow phone screen in the middle of the page.

12. ✅ **No loading state on booking form submission**
    After the user clicks "Потвърди часа" on `booking_appointment`, the button stays active with no spinner or disabled state while the API call is in flight. A user can double-click and submit twice. Disable the button and show a loading indicator on submit.

13. ✅ **No client-side booking cancellation**
    Users can see their bookings in `my_appointments` but cannot cancel a pending booking themselves. They have to contact the consultant separately. Added cancel button in `my_appointments` for pending bookings; DELETE `/api/book/{id}` endpoint verifies JWT ownership before setting status to `cancelled`.

14. **Confirmation email has no calendar attachment**
    When a consultant confirms a booking, the client gets a plain HTML email but no `.ics` file. Add an ICS attachment so clients can click once to add it to Google Calendar / Apple Calendar / Outlook.

15. ✅ **No admin dashboard**
    The config defines `ADMIN_EMAILS` and the auth route returns `role: admin`, but there is no admin UI. Added `frontend/admin/index.html` — shows all bookings with status/consultant filters, stats row, and confirm/decline actions for pending bookings. Backend: `GET /api/admin/bookings` + `PATCH /api/admin/bookings/{id}` in `backend/routes/admin.py`, guarded by `ADMIN_EMAILS`.

16. ✅ **`booking_confirmed` page details are hardcoded / not populated from URL state**
    The "Детайли за срещата" card on `booking_confirmed` shows empty or static placeholder text unless the booking form explicitly populates it. If the user lands there via a direct link or page refresh, the card is blank.

---

## Backend / Code Quality

17. ✅ **`@app.on_event("startup"/"shutdown")` is deprecated**
    Migrated `backend/main.py` to use `@asynccontextmanager` lifespan. Startup and shutdown logic are now in a single `lifespan()` function passed to `FastAPI(lifespan=lifespan)`.

18. ✅ **`_html_page` for confirm/decline has no branding**
    Replaced plain white page with a branded page: Gfinance logo, Material icon, card layout, "Към началната страница" button.

19. ✅ **Duplicate router import in `main.py`**
    Extracted Vercel POST handler logic into `handle_vercel_booking()` (public) in `routes/booking.py`. `main.py` now only imports `router` and `handle_vercel_booking` — no private helpers, no `BookRequest` re-import.

20. ✅ **Phone number stored inside the `notes` field**
    `client_phone` is now stored in its own column. **Requires one manual SQL step in Supabase SQL Editor:**
    ```sql
    ALTER TABLE bookings ADD COLUMN IF NOT EXISTS client_phone TEXT NOT NULL DEFAULT '';
    ```
    Admin dashboard shows phone number in its own row on each booking card.
