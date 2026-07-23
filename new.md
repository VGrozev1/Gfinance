# Gfinance – Next Improvements

---

## Quick Wins (high impact, low effort)

1. **Page titles are still generic on most subpages** *(SEO)*
   - `consultants_info`: `<title>Gfinance Consultants</title>` → "Нашите консултанти – Gfinance"
   - `credit_info`: → "Информация за кредити и ипотеки – Gfinance"
   - `booking_appointment`: → "Запази безплатна консултация – Gfinance"
   - `credit_calculator`: → "Кредитен калкулатор – изчисли вноската си – Gfinance"
   - Descriptions should mention "Бургас", the service, and "безплатна консултация"

2. **No WhatsApp / Viber contact option** *(UX / conversion)*
   - Many Bulgarian users prefer messaging apps over phone calls
   - Add a floating WhatsApp button (or Viber) next to the existing phone CTA on mobile
   - `wa.me/359888152181` — no account needed, just the link
   - Can also appear in the contact section on the homepage

3. **No social proof numbers on homepage** *(conversion)*
   - Add a "trust bar" row below the hero: e.g. "10+ банки сравнени", "Безплатна консултация", "Бургас & онлайн"
   - Static HTML, no backend needed — just honest round numbers from the business

4. **Consultant photos are PNG — should be WebP** *(performance)*
   - `georgi-grozev.png`, `petya-grozeva.png`, `irina-panayotova.png` are uncompressed PNGs
   - Convert to WebP (usually 60–80% smaller) with `cwebp` or `sips`
   - Add `<img src="photo.webp" loading="lazy" width="X" height="Y">` with explicit dimensions to prevent layout shift
   - Improves Core Web Vitals score, which is a Google ranking signal

5. **`robots.txt` Disallow paths are wrong** *(SEO)*
   - Currently `Disallow: /confirm` and `Disallow: /decline` — these paths don't exist
   - Actual routes are `/api/book/confirm` and `/api/book/decline`
   - Fix in `frontend/robots.txt`

6. **`consultants_info` page has English lang and heading** *(SEO + accessibility)*
   - `frontend/consultants_info/index.html` — `<html lang="en">` should be `lang="bg"`
   - `<title>Gfinance Consultants</title>` and `<h1>Gfinance Consultants</h1>` should be Bulgarian
   - Google uses these for search snippets

7. **Petya Grozeva has placeholder title "Специалист мама"** *(content)*
   - `frontend/my_appointments/index.html:99` and `frontend/booking_appointment/index.html:99`
   - Replace with her actual title (e.g. "Кредитен консултант")

8. **`my_profile` has hardcoded fake data** *(UX)*
   - "Последна промяна преди 3 месеца" is static text, never updates
   - "2 нови" badge next to Appointments is hardcoded
   - Either remove or wire to real Supabase data

---

## Medium Effort

9. **No FAQ section** *(SEO + UX)*
   - Add a collapsible FAQ accordion to `credit_info` or as a standalone section on the homepage
   - Target questions: "Колко трае одобрението?", "Безплатно ли е?", "Как работи консултантът?", "Нужен ли ми е поръчител?"
   - Add `FAQPage` JSON-LD schema — Google shows these as expandable rich results in search, huge click-through boost
   - Example: `{ "@type": "FAQPage", "mainEntity": [{ "@type": "Question", "name": "...", "acceptedAnswer": { "@type": "Answer", "text": "..." } }] }`

10. **Calculator has no PDF/share of results** *(UX)*
    - After calculating, users can't save or send the result to a partner or family member
    - Add a "Сподели / Запази" button that opens a printable summary or copies a URL with params pre-filled
    - URL params (`?amount=&months=&rate=`) are already partially in place from the shareable link feature

11. **Blog has no search or category filter** *(UX)*
    - As article count grows, users can't find what they need
    - Add a simple client-side filter on `blog/index.html` by tag (ипотека, рефинансиране, документи, калкулатор)
    - Static JS — no backend needed

12. **No newsletter / email capture** *(conversion + retention)*
    - Users who read a blog article and leave are lost forever
    - Add a simple email signup box at the bottom of blog articles and on the homepage: "Получавай съвети за кредити — без спам"
    - Backend: one Supabase table (`newsletter_subscribers`) + one API endpoint
    - Optionally integrate with MailerLite (free tier, has BG UI)

13. **Booking form has no step indicator** *(UX)*
    - `booking_appointment` is a single long scroll — users don't know how many steps there are
    - Add a step bar at the top: "1. Избери консултант → 2. Избери дата и час → 3. Въведи данни → 4. Потвърди"
    - Pure HTML/CSS — no logic change needed

14. **No testimonials / client reviews on homepage** *(conversion + SEO)*
    - The homepage has no social proof from real clients
    - Add a "Какво казват клиентите ни" section with 3–4 quote cards
    - Can be static initially; later wire to a `reviews` Supabase table
    - Add `Review` JSON-LD schema for rich results

---

## SEO — Remaining Actions

15. **Backlinks — zero external sites link to gfinance.bg** *(SEO, biggest long-term factor)*
    - Register on: `goldenpages.bg`, `biznes.bg`, `yelp.bg`, `zaplata.bg` — each gives a do-follow backlink
    - Create a Facebook Business page and a LinkedIn company page with the website link
    - Ask a Бургас real estate agency or notary to add Gfinance to their "useful links" page
    - Target: 10–20 quality Bulgarian backlinks in the first 3 months

16. **Only 4 blog articles — need 10+ to rank** *(SEO)*
    - Google favors sites with consistent fresh content
    - Next article ideas:
      - "Каква е разликата между ГПР и лихвен процент?"
      - "Как банките оценяват кредитоспособността ти"
      - "5 грешки при теглене на кредит"
      - "Може ли да тегля кредит с поръчител?"
      - "Ипотечен кредит при свободна практика — как работи?"
      - "Кой кредит е по-добър за ремонт: жилищен или потребителски?"
    - Aim: 1–2 articles per month

17. **Core Web Vitals — images below fold have no `loading="lazy"`** *(SEO / performance)*
    - All `<img>` tags that appear below the visible screen on load should have `loading="lazy"`
    - Also add `width` and `height` to every `<img>` to eliminate Cumulative Layout Shift (CLS)
    - Check score at `pagespeed.web.dev` with the live URL — target 90+ on all metrics

18. **Google Search Console not verified yet** *(SEO)*
    - Without GSC, Google can't tell you which queries bring traffic or what's broken
    - Add `<meta name="google-site-verification" content="YOUR_CODE">` to `frontend/index.html`
    - Submit `sitemap.xml` once verified

---

## Larger Features

19. **No appointment reminder emails** *(retention)*
    - After a booking is confirmed, neither client nor consultant gets a reminder before the appointment
    - Options: Supabase Edge Functions with `pg_cron`, or external service (n8n, Make.com, Zapier — all have free tiers)
    - Trigger: send email 24h before `booking_date` where `status = 'confirmed'`

20. **Admin has no calendar view** *(admin UX)*
    - Current admin dashboard is a flat list of bookings
    - A weekly calendar grid (Mon–Fri, 9:00–18:00) per consultant would let admins spot gaps and double-bookings at a glance
    - Frontend-only with existing `/api/admin/bookings` data

21. **No cancellation reason collected** *(business insight)*
    - When a client or admin cancels a booking, there's no reason captured
    - Add a short dropdown on cancel: "Клиентът се отказа", "Консултантът не е наличен", "Грешен час", "Друго"
    - Store in `bookings.cancel_reason TEXT`; visible in admin dashboard

22. **Credit info page is static — no comparison tool** *(product)*
    - Users on `credit_info` read text but can't act — no way to compare two loan types side by side
    - Add a simple side-by-side scenario comparer: two columns, each with Amount / Term / Rate inputs, showing monthly payment and total interest
    - Drives users toward booking a consultation to explore further

23. **No offline / PWA support** *(mobile UX)*
    - On slow mobile connections the site is blank until assets load
    - A basic Service Worker can cache the shell (CSS, fonts, logo) so repeat visits are instant
    - Also enables "Add to Home Screen" for users who visit frequently
    - `frontend/sw.js` + `<script>navigator.serviceWorker.register('/sw.js')</script>` in every page
