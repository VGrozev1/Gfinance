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

8. ✅ **External stock images from `lh3.googleusercontent.com/aida-public`**
   Skipped — will replace with owned images when available.

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

14. ✅ **Confirmation email has no calendar attachment** *(skipped — keeping it basic)*

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

---

## Bugs Found (not yet fixed)

21. **`consultants_info` page has English `lang`, title, and heading** *(SEO + accessibility)*
    - `frontend/consultants_info/index.html:3` — `<html lang="en">` should be `lang="bg"`
    - `<title>Gfinance Consultants</title>` should be Bulgarian
    - `<h1>Gfinance Consultants</h1>` same — Google uses this for search snippets

22. **Petya Grozeva has placeholder title "Специалист мама"** *(content)*
    - Appears in `frontend/my_appointments/index.html:99` and `frontend/booking_appointment/index.html:99`
    - Should be her actual professional title (e.g. "Кредитен консултант")

23. **Hardcoded fake data in `my_profile`** *(UX)*
    - `frontend/my_profile/index.html:122` — "Последна промяна преди 3 месеца" is static text, never updates
    - `frontend/my_profile/index.html:140` — "2 нови" badge next to Appointments is hardcoded, not a real count
    - Both should either be removed or wired to real data

24. **`robots.txt` disallows wrong paths for confirm/decline** *(SEO)*
    - Currently: `Disallow: /confirm` and `Disallow: /decline`
    - Actual routes are `/api/book/confirm` and `/api/book/decline` — the current rules do nothing
    - Fix to: `Disallow: /api/book/confirm` and `Disallow: /api/book/decline`

25. **`frontend/homepage/homepage.html` is a dead duplicate** *(maintenance)*
    - Served at `/homepage/` which is never linked anywhere in the app
    - Still uses Tailwind CDN (not the compiled CSS), has "© 2024" copyright
    - Should be deleted — `frontend/index.html` is the real homepage

26. **Subpage navigation drawers are missing profile/appointments links** *(UX)*
    - All subpages (`booking_appointment`, `credit_info`, `consultants_info`, etc.) have a hamburger menu that only shows: Начало, Експерти, Кредити, Калкулатор, Запис, Вход
    - Logged-in users have no way to reach "Моят профил" or "Моите срещи" from any subpage without going back to the homepage first

27. **`booking_confirmed` shows dashes when accessed directly** *(UX)*
    - If a user navigates to `/booking_confirmed` directly or refreshes after booking, all fields show "—" because `sessionStorage.lastBooking` is gone
    - Should show a generic "Заявката ви е изпратена" message instead of empty fields

---

## New Improvements

28. ✅ **Guest booking: no reference number shown on confirmation** *(UX)*
    - When a guest (not logged in) books, they see the confirmation page but have no booking ID or reference number
    - They have no way to reference the booking if they want to cancel it later (no account = no "Моите срещи")
    - `booking_appointment` now stores `booking_id` and `is_guest` in sessionStorage; `booking_confirmed` shows the reference number and a "Създай профил" CTA for guest users

29. ✅ **Service type is hardcoded as "Кредитна консултация"** *(UX)*
    - `booking_appointment/index.html` always sends `service: 'Кредитна консултация'` regardless of what the user needs
    - Replaced with a dropdown: Жилищен кредит, Потребителски кредит, Рефинансиране, Ипотека, Бизнес финансиране, Друго

30. **No booking reminder emails** *(feature)*
    - After a booking is confirmed, neither the client nor the consultant receives a reminder before the appointment
    - Add a background job or Supabase cron that sends a reminder 24h before each confirmed booking
    - *Deferred: not feasible on Vercel serverless without an external cron/queue service*

31. ✅ **No password reset flow** *(UX)*
    - `login/index.html` already has "Забравена парола?" modal using `supabase.auth.resetPasswordForEmail()`

32. ✅ **Admin: confirm/decline doesn't send emails** *(feature)*
    - When an admin clicks Confirm or Decline in the admin dashboard, it updates the status in the DB
    - `backend/routes/admin.py` now sends confirmation/decline email via `BackgroundTasks` on status change

33. ✅ **No "Запиши час" CTA on consultants_info page** *(UX)*
    - Each consultant card now has a "Запиши час" button linking to `/booking_appointment?consultant=ID`
    - `booking_appointment` reads `?consultant=` URL param and pre-selects that consultant on load

34. ✅ **Credit calculator results not shareable** *(UX)*
    - Added "Копирай линк" button (link icon) that encodes `?amount=`, `?months=`, `?rate=` into the URL
    - On load, URL params are read back and pre-fill the inputs; check icon confirms copy success

---

## SEO — Step-by-Step Guide to Rank Higher

These are actions ranked from highest to lowest impact. Do them in order.

### Step 1 ✅ — Google Search Console
1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Add `https://gfinance.bg` as a property
3. Verify ownership via the HTML tag method — add `<meta name="google-site-verification" content="YOUR_CODE"/>` to `frontend/index.html`
4. Submit your sitemap: enter `https://gfinance.bg/sitemap.xml` in the Sitemaps section
5. Check "Coverage" after 2–3 days to see if all pages are indexed
6. **Why it matters:** Google can't rank pages it hasn't found. Search Console tells you exactly what Google sees and what's broken.

### Step 2 ✅ — Google Business Profile
1. Go to [business.google.com](https://business.google.com) and create a profile for Gfinance
2. Fill in: business name (Gfinance), category (Финансов консултант / Financial Consultant), address (Бургас, ул. Поп Груйо 66А), phone, website, hours
3. Verify via postcard or phone
4. Add photos: office, consultants, logo
5. Ask your first 5 clients to leave a Google review
6. **Why it matters:** Google Business Profile is how you appear in Google Maps and in the local "3-pack" results — the box with 3 businesses that shows up before regular search results for "кредитен консултант Бургас"

### Step 3 ✅ — Add Schema.org structured data to the homepage
Structured data tells Google exactly what your business is. Add this JSON-LD block inside `<head>` of `frontend/index.html`:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FinancialService",
  "name": "Gfinance",
  "description": "Вашият доверен партньор в кредитирането. Консултации за жилищни и потребителски кредити в Бургас.",
  "url": "https://gfinance.bg",
  "telephone": "+359888152181",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ул. Поп Груйо 66А",
    "addressLocality": "Бургас",
    "addressCountry": "BG"
  },
  "openingHours": "Mo-Fr 09:00-18:00",
  "image": "https://gfinance.bg/assets/images/logo-icon.png",
  "areaServed": "Бургас",
  "priceRange": "Безплатно"
}
</script>
```
**Why it matters:** Google uses this to show rich results (star ratings, address, phone) directly in search — which increases click-through rate by 20–30%.

### Step 4 — Improve page titles and descriptions for each page
Each page's `<title>` and `<meta name="description">` is your ad in Google search results. Currently they're generic.

Recommended changes:
| Page | Current title | Better title |
|------|--------------|--------------|
| Homepage | Gfinance | Кредитен консултант Бургас – Gfinance |
| consultants_info | Gfinance Consultants | Нашите експерти – Gfinance |
| credit_info | Информация за кредити – Gfinance | Кредити и ипотеки – сравни и избери – Gfinance |
| booking_appointment | Запис на час – Gfinance | Запази консултация безплатно – Gfinance |

For descriptions: include the city (Бургас), the service (кредитна консултация), and a benefit (безплатна, без ангажимент).

### Step 5 — Target local keywords in page content
Add these phrases naturally in the text of `credit_info` and `consultants_info`:
- "кредитен консултант Бургас"
- "ипотечен кредит Бургас"
- "потребителски кредит консултация"
- "рефинансиране на кредит"
- "безплатна кредитна консултация"

Google ranks pages for terms that appear in their content. If these words aren't on your pages, you won't rank for them.

### Step 6 — Build backlinks (ongoing, biggest long-term factor)
Backlinks (other sites linking to yours) are the #1 ranking factor after page content.

Easy first links to get:
1. **Local business directories:** Register on zaplata.bg, yelp.bg, goldenpages.bg, biznes.bg with your website URL
2. **Facebook page:** Create a Facebook business page for Gfinance, add website link, post regularly
3. **LinkedIn:** Create a company page, link to gfinance.bg
4. **Partner sites:** Ask mortgage brokers, real estate agencies, or accountants in Бургас to add you to their "useful links" page
5. **Local news:** Reach out to local Бургас news sites (Burgasinfo.bg, Focus-news.net) for a small feature or listing

**Target:** aim for 10–20 quality Bulgarian backlinks in the first 3 months.

### Step 7 — Add a blog or articles section
Google strongly favors sites that publish fresh, useful content.

Article ideas that match what people search for:
- "Как да изберем ипотечен кредит през 2026"
- "Разлика между ипотечен и потребителски кредит"
- "Кога си струва да рефинансираш кредита си"
- "Какви документи са нужни за кредит"

Even 4–6 articles (500–800 words each) will significantly increase the number of keywords you rank for. Host them at `/blog/article-slug`.

### Step 8 — Core Web Vitals (technical performance)
Google uses page speed as a ranking signal.

Check your scores at [pagespeed.web.dev](2 with your live URL. Target: all scores above 90.

Current optimizations already done: compiled Tailwind CSS, no CDN JS frameworks on most pages.
Remaining quick wins:
- Add `loading="lazy"` to all `<img>` tags below the fold
- Add explicit `width` and `height` attributes to images to prevent layout shift
- Consider converting consultant photos to WebP format (smaller file size)

### Step 9 — Get and respond to Google reviews
Reviews directly affect Local Pack ranking.

Action plan:
1. After each consultation, send a follow-up email with a direct Google review link
2. Aim for 10+ reviews with 4.5+ average in the first 3 months
3. Respond to every review (even negative ones) — Google rewards engagement

### Step 10 — Monitor and iterate (monthly)
1. Check Google Search Console weekly: which queries bring traffic? What pages get impressions but no clicks? (Those need better titles/descriptions.)
2. Check Google Analytics (add it to the site — free): where do users drop off?
3. Every month: publish one new article, respond to new reviews, check for new backlink opportunities
4. Track your position for "кредитен консултант Бургас" — it should improve within 3–6 months if you follow Steps 1–7
