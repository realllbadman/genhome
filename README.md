# GenHome — Generator Sales Website

A full-stack e-commerce style website for generator sales. Customers can browse 120+ generators, add to cart, place orders, and request quotes. The owner receives instant email alerts for every order and quote, and manages everything from a password-protected admin panel.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + SQLAlchemy + SQLite |
| Frontend | Plain HTML / CSS / JS |
| Email | aiosmtplib (async Gmail SMTP) |
| Live Chat | Tawk.to |
| Server | Uvicorn (ASGI) |

---

## Project Structure

```
project/
├── frontend/
│   ├── index.html        # Main store (products, cart, order form, quote modal)
│   ├── products.js       # 120 products catalog
│   ├── admin.html        # Admin panel (orders + quotes tabs)
│   └── about.html        # About Us page
├── backend/
│   ├── main.py           # FastAPI app, CORS, routes, static files
│   ├── database.py       # SQLite engine + session
│   ├── models.py         # Booking + Order ORM models
│   ├── schemas.py        # Pydantic schemas
│   ├── routes/
│   │   ├── bookings.py   # POST /api/bookings — quote requests
│   │   ├── orders.py     # POST /api/orders — cart orders
│   │   └── admin.py      # GET/PATCH/DELETE /api/admin/* (Basic Auth)
│   └── services/
│       └── email.py      # Customer + owner email notifications
├── .env                  # Secrets — NOT in git
├── .env.example          # Template for .env
├── requirements.txt
└── README.md
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/realllbadman/genhome.git
cd genhome/project
```

### 2. Create virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Fill in your credentials (see sections below).

---

## Configuring .env

### SMTP — Email Notifications (Gmail)

Gmail requires an **App Password** (not your regular password).

1. Go to your Google Account → **Security**
2. Enable **2-Step Verification**
3. Go to **Security → App Passwords** → generate one for "GenHome"
4. Fill in `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.gmail@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
OWNER_EMAIL=your.gmail@gmail.com
BUSINESS_EMAIL=your.gmail@gmail.com
OWNER_PHONE=+1 (000) 000-0000
```

### Admin Credentials

```env
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_strong_password
```

### Database

```env
DATABASE_URL=sqlite:///./bookings.db
```

---

## Running Locally

```bash
uvicorn backend.main:app --reload --port 8001
```

| URL | Page |
|---|---|
| http://localhost:8001 | Store |
| http://localhost:8001/admin | Admin panel |
| http://localhost:8001/about | About Us |
| http://localhost:8001/docs | FastAPI API docs |

---

## Deployment (Hostinger VPS)

```bash
ssh root@YOUR_VPS_IP
git clone https://github.com/realllbadman/genhome.git
cd genhome/project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
nano .env   # add all environment variables
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

To update the live site after pushing changes:

```bash
git pull
# restart uvicorn
```

---

## API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/bookings/` | None | Submit a quote request |
| `POST` | `/api/orders` | None | Submit a cart order |
| `GET` | `/api/admin/bookings` | Basic | List all quotes |
| `GET` | `/api/admin/bookings/{id}` | Basic | Get single quote |
| `PATCH` | `/api/admin/bookings/{id}` | Basic | Update quote status/notes |
| `DELETE` | `/api/admin/bookings/{id}` | Basic | Delete a quote |
| `GET` | `/api/admin/orders` | Basic | List all orders |
| `GET` | `/api/admin/orders/{id}` | Basic | Get single order |
| `PATCH` | `/api/admin/orders/{id}` | Basic | Update order status/notes |
| `DELETE` | `/api/admin/orders/{id}` | Basic | Delete an order |
| `GET` | `/api/admin/stats` | Basic | Dashboard summary counts |

---

## Key Business Rules

- **Free shipping** on orders over $2,500
- **$300 flat rate** shipping on orders under $2,500
- **Admin panel** at `/admin` — protected by HTTP Basic Auth
- **Products** managed in `frontend/products.js` — 120 products, 5 categories
