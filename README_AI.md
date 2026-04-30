# README_AI.md — AI Continuation Memory
> This file is the single source of truth for any AI (Claude, Gemini, or other) continuing work on this project.
> Update this file after EVERY change made.

---

## 1. PROJECT OVERVIEW

**Name:** GenHome Sales
**Domain:** genhomesales.com
**Purpose:** E-commerce style website for selling diesel generators and industrial power equipment.
**Owner contact:** genhome41@gmail.com | +1 (601) 601-3408

Customers can:
- Browse 80 generator products across 5 categories
- Add to cart and place orders
- Request a quote
- Contact via WhatsApp, TikTok, Facebook, Email

Owner receives:
- Email notification on every order and quote request
- Admin panel to manage orders and quotes

---

## 2. ARCHITECTURE

```
project/
├── backend/
│   ├── main.py              # FastAPI app entry point, routes, static file serving
│   ├── database.py          # SQLAlchemy engine + session (SQLite)
│   ├── models.py            # DB models: Booking, Order
│   ├── schemas.py           # Pydantic schemas for request/response validation
│   ├── requirements.txt     # Python dependencies
│   └── routes/
│       ├── bookings.py      # POST /api/bookings — quote requests
│       ├── orders.py        # POST /api/orders — cart orders
│       └── admin.py         # GET/PATCH/DELETE /api/admin/* — admin CRUD
│   └── services/
│       └── email.py         # Gmail SMTP email sending (customer + owner notifications)
│
├── frontend/
│   ├── index.html           # Main store — ALL UI in one file (nav, hero, products, cart, modals)
│   ├── products.js          # 80 products array (loaded as static file)
│   ├── admin.html           # Admin dashboard (orders + quotes tabs)
│   └── about.html           # About Us standalone page
│
├── .env                     # Secrets — NOT in git
├── .env.example             # Placeholder template for .env
├── .gitignore               # Excludes .env, *.db, __pycache__, .venv
└── README_AI.md             # This file
```

---

## 3. BACKEND DETAILS

**Framework:** FastAPI + Uvicorn
**Database:** SQLite via SQLAlchemy (file: bookings.db)
**Email:** Gmail SMTP (smtp.gmail.com:587) with App Password

### Routes
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/bookings/ | Submit quote request |
| POST | /api/orders | Submit cart order |
| GET | /api/admin/stats | Dashboard stats |
| GET | /api/admin/bookings | All quotes |
| GET | /api/admin/bookings/{id} | Single quote |
| PATCH | /api/admin/bookings/{id} | Update quote status/notes |
| DELETE | /api/admin/bookings/{id} | Delete quote |
| GET | /api/admin/orders | All orders |
| GET | /api/admin/orders/{id} | Single order |
| PATCH | /api/admin/orders/{id} | Update order status/notes |
| DELETE | /api/admin/orders/{id} | Delete order |
| GET | / | Serves index.html |
| GET | /admin | Serves admin.html |
| GET | /about | Serves about.html |

### DB Models
- **Booking:** id, first_name, last_name, phone, email, service, preferred_date, generator_size, details, status, created_at, notes
- **Order:** id, first_name, last_name, phone, email, company, address, city, state, zip, contact_pref, best_time, notes, items (JSON string), total, status, created_at

### Email
- `send_customer_confirmation()` — sent to customer after quote
- `send_owner_notification()` — sent to owner after quote
- `send_order_customer_confirmation()` — sent to customer after order
- `send_order_owner_notification()` — sent to owner after order

---

## 4. FRONTEND DETAILS

**Stack:** Plain HTML + CSS + Vanilla JavaScript (no frameworks)
**Single file:** index.html contains all styles, HTML, and JS

### Key JS Functions
| Function | Purpose |
|----------|---------|
| `renderProducts(list)` | Renders product cards to grid |
| `applyFilters()` | Filters by category, brand, fuel, kW range, sort |
| `handleSearch(q)` | Triggers search from nav/hero bar |
| `fuzzyMatch(q, p)` | Levenshtein fuzzy search (tolerance: 0/1/2) |
| `showSuggestions(q, id)` | Shows autocomplete dropdown |
| `addToCart(id)` | Adds product, saves to localStorage, shows toast |
| `show('cart')` | Opens cart page overlay, sets URL hash #cart |
| `openProductModal(id)` | Opens product detail modal |
| `openQuote(id)` | Opens quote modal (pre-fills product if id given) |
| `submitQuote()` | POST to /api/bookings/ |
| `submitOrder()` | POST to /api/orders |
| `getShipping()` | Returns 0 if subtotal >= $2500, else $150 |
| `getPaymentMethod()` | Returns selected payment option |
| `saveCart()` | Persists cart to localStorage (key: gh_cart) |

### Product Schema (products.js)
```js
{
  id: string,
  name: string,
  brand: string,           // Yanmar, Honda, Generac, Kohler, Cummins, etc.
  category: string,        // home-standby, commercial, industrial, portable, inverter
  kw: number,
  fuel: string,
  price: number,
  originalPrice: number,
  description: string,
  features: string[],
  inStock: boolean,
  badge: null | "New" | "Best Seller",
  image: string,           // direct image URL
  imageSearch: string      // search description
}
```

### Search System
- Fuzzy Levenshtein search across name, brand, category, fuel
- Tolerance: query ≤2 chars → 0, ≤4 → 1, >4 → 2
- Autocomplete suggestions (max 6) shown in dropdown
- Two search bars: nav (top) and hero (middle of page)

### Cart
- Stored in `localStorage` key `gh_cart`
- Persists across page refresh
- URL hash `#cart` reopens cart on refresh
- Free shipping on orders over $2,500, otherwise $150

### Payment Options
Radio buttons: Bank Transfer, Apple Pay, Chime, Zelle, Other (with text input)

---

## 5. CURRENT STATE

### Working
- Full product browsing, filtering, sorting
- Fuzzy search with autocomplete on both search bars
- Add to cart, cart persistence, order form submission
- Quote request form
- Email notifications (customer + owner) for both orders and quotes
- Admin panel: view/update/delete orders and quotes
- About Us page (/about)
- Mobile nav (partial — cart icon not visible on some mobile views)
- Social links: WhatsApp (wa.me/message/GUYDIOVVVAZAJ1), TikTok (@genhome6), Facebook

### Incomplete / Known Issues
- **Mobile layout** — not fully responsive; cart icon missing on iPhone, layout breaks on small screens
- **No HTTPS** — domain genhomesales.com shows "Not secure" (SSL not configured on VPS)
- **Chatbot** — currently using a third-party widget (visible in screenshots); not custom built
- **Product images** — some products use stock/placeholder images that may not display correctly
- **Search** — could be improved with better ranking and filters

---

## 6. DEPLOYMENT

- **VPS:** Hostinger VPS
- **Domain:** genhomesales.com (registered on Namecheap)
- **GitHub:** https://github.com/realllbadman/genhome (Private)
- **Run command:** `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
- **SSL:** Not yet configured (needs Nginx + Certbot)
- **.env on VPS:** Must be created manually (not in git)

### Environment Variables Required
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=genhome41@gmail.com
SMTP_PASSWORD=<gmail app password>
OWNER_EMAIL=genhome41@gmail.com
BUSINESS_EMAIL=genhome41@gmail.com
OWNER_PHONE=+1 (601) 601-3408
ADMIN_USERNAME=genhome_admin
ADMIN_PASSWORD=GenHome@2026!
DATABASE_URL=sqlite:///./bookings.db
```

---

## 7. DEVELOPMENT RULES

- Do NOT break existing features when adding new ones
- Do NOT add frameworks (React, Vue, etc.) — keep plain HTML/JS
- Do NOT push `.env` or `*.db` to GitHub
- After every change: run `git add . && git commit -m "..." && git push`
- Test on both desktop and mobile after UI changes
- Keep products.js as the single source of product truth
- Admin panel auth is HTTP Basic Auth (credentials in .env)

---

## 8. NEXT PRIORITIES (in order)

1. **Mobile responsiveness** — fix nav, product grid, cart, modals for small screens
2. **SSL/HTTPS** — set up Nginx reverse proxy + Certbot on VPS
3. **Chatbot** — integrate new/custom chatbot
4. **Add products** — expand catalog beyond 80 products
5. **Improve search** — better ranking, filter UX

---

## 9. LAST UPDATE

**Date:** 2026-04-30
**Changes:** Created README_AI.md — full project documentation for AI continuity
**Reason:** Establishing shared memory between Claude Code and other AI systems
**Files:** README_AI.md (created)
