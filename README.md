# GenHome — Generator Business Website

A full-stack booking and management website for a generator sales, rental, and servicing business. Customers can browse services and submit booking requests. The owner receives instant email and SMS alerts for every new booking and manages everything from a password-protected admin panel.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + SQLAlchemy + SQLite |
| Frontend | Plain HTML / CSS / JS (single-page) |
| Email | aiosmtplib (async SMTP) |
| SMS | Twilio Python SDK |
| Live Chat | Tawk.to (free embed) |
| Server | Uvicorn (ASGI) |

---

## Project Structure

```
project/
├── frontend/
│   ├── index.html        # Main public website (SPA — 6 sections)
│   └── admin.html        # Admin panel (login + dashboard)
├── backend/
│   ├── main.py           # FastAPI app, CORS, routes, static files
│   ├── database.py       # SQLite engine + session
│   ├── models.py         # Booking ORM model
│   ├── schemas.py        # Pydantic schemas
│   ├── routes/
│   │   ├── bookings.py   # POST /api/bookings
│   │   └── admin.py      # GET/PATCH/DELETE /api/admin/*  (Basic Auth)
│   └── services/
│       ├── email.py      # Customer confirmation + owner notification emails
│       └── sms.py        # Owner SMS alert via Twilio
├── .env.example
├── requirements.txt
└── README.md
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO/project
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` in your editor and fill in your credentials (see sections below).

---

## Configuring .env

### SMTP — Email Notifications (Gmail)

Gmail requires an **App Password** (not your regular password) when using third-party apps.

1. Go to your Google Account → **Security**
2. Enable **2-Step Verification** if not already on
3. Go to **Security → App Passwords**
4. Under "Select app" choose **Mail**, under "Select device" choose **Other** and type `GenHome`
5. Click **Generate** — copy the 16-character password shown
6. Fill in `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.gmail@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop      # the 16-char App Password (spaces are fine)
OWNER_EMAIL=your.gmail@gmail.com       # where owner notification emails go
BUSINESS_EMAIL=your.gmail@gmail.com   # shown in email footer
```

> **Note:** If you use another provider (Outlook, SendGrid, etc.), update `SMTP_HOST` and `SMTP_PORT` accordingly.

---

### Twilio — SMS Notifications

Twilio offers a free trial that includes enough credits to test SMS.

1. Sign up at [twilio.com](https://www.twilio.com) (free — no credit card required for trial)
2. From the **Console Dashboard**, copy your **Account SID** and **Auth Token**
3. Go to **Phone Numbers → Manage → Buy a Number** — get a free trial number
4. Fill in `.env`:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_FROM_NUMBER=+15551234567    # your Twilio trial number
OWNER_PHONE=+15557654321           # your real mobile number (must be verified on trial)
```

> **Trial account note:** On a free Twilio trial, you can only send SMS to verified numbers. Go to **Verified Caller IDs** in the console to add your mobile number.

---

### Admin Credentials

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme123    # CHANGE THIS before going live
```

Choose a strong password — this protects all customer data.

---

### Database

```env
DATABASE_URL=sqlite:///./bookings.db
```

The SQLite file (`bookings.db`) is created automatically in the project directory on first run. No setup required.

---

## Running Locally

```bash
uvicorn backend.main:app --reload
```

| URL | Page |
|---|---|
| http://localhost:8000 | Public website |
| http://localhost:8000/admin | Admin panel |
| http://localhost:8000/docs | FastAPI interactive API docs |

The `--reload` flag watches for file changes and restarts automatically — useful during development.

---

## Setting Up Tawk.to Live Chat

Tawk.to provides free unlimited live chat for your website.

1. Sign up free at [tawk.to](https://www.tawk.to)
2. Create a **Property** and give it your business name
3. Copy the JavaScript embed snippet from **Administration → Chat Widget**
4. Open `frontend/index.html` and scroll to the very bottom
5. Find this comment block:

```html
<!--
  TAWK.TO LIVE CHAT
  ...
-->
<script>/* Paste your Tawk.to embed script here */</script>
```

6. Replace the `<script>/* Paste your Tawk.to embed script here */</script>` line with the snippet from Tawk.to

The **"Chat with Us Live"** button on the Contact page will then open the chat widget automatically (`Tawk_API.toggle()`).

---

## Replacing Gallery Placeholders

The gallery section in `frontend/index.html` currently uses emoji placeholders. To replace them with real photos:

1. Place your images in `frontend/` (e.g. `frontend/gallery-1.jpg`)
2. Find the gallery items in `index.html` — each looks like:

```html
<div class="gallery-item">
  <div class="gallery-bg gi-1">🏭</div>
  <div class="gallery-overlay"><span>Industrial Installation</span></div>
</div>
```

3. Replace the inner `<div class="gallery-bg ...">` with an `<img>` tag:

```html
<div class="gallery-item">
  <img src="/static/gallery-1.jpg" alt="Industrial Installation"
       style="width:100%;height:100%;object-fit:cover;" />
  <div class="gallery-overlay"><span>Industrial Installation</span></div>
</div>
```

**Recommended image sizes:**
- Featured item (spans 2 columns): **1200 × 900 px**
- Standard items: **600 × 450 px**
- Format: JPEG at 80–85% quality for best file size/quality balance

---

## Deploying to Render.com (Free Tier)

Render offers free hosting for Python web services with zero configuration.

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

> Make sure `.env` is in your `.gitignore` — never commit real credentials.

### Step 2 — Create a Web Service on Render

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **New → Web Service**
3. Connect your GitHub account and select your repository
4. Configure the service:

| Setting | Value |
|---|---|
| **Environment** | Python 3 |
| **Root Directory** | `project` (if your repo root is the parent folder) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |

### Step 3 — Set Environment Variables

In the Render dashboard → your service → **Environment**:

Add every variable from your `.env` file:

```
SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
OWNER_EMAIL, BUSINESS_EMAIL,
TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, OWNER_PHONE,
ADMIN_USERNAME, ADMIN_PASSWORD,
DATABASE_URL=sqlite:///./bookings.db
```

### Step 4 — Deploy

Click **Create Web Service**. Render will build and deploy automatically. Every `git push` to `main` triggers a redeploy.

Your site will be live at: `https://your-service-name.onrender.com`

> **Important — SQLite in production:** The SQLite database file lives on Render's ephemeral disk. It will be **wiped on every redeploy**. For a production site with real bookings, migrate to PostgreSQL:
> - Add a Render Postgres database (free tier available)
> - Update `DATABASE_URL` to the Postgres connection string Render provides
> - Remove the `connect_args={"check_same_thread": False}` line from `database.py`
> - Add `psycopg2-binary` to `requirements.txt`

---

## API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/bookings/` | None | Submit a booking request |
| `GET` | `/api/admin/bookings` | Basic | List all bookings (filterable) |
| `GET` | `/api/admin/bookings/{id}` | Basic | Get single booking |
| `PATCH` | `/api/admin/bookings/{id}` | Basic | Update status / notes |
| `DELETE` | `/api/admin/bookings/{id}` | Basic | Delete a booking |
| `GET` | `/api/admin/stats` | Basic | Booking summary counts |

Interactive docs available at `/docs` (FastAPI Swagger UI) when running locally.

---

## Phase 2 Roadmap

Future features planned for the next development phase:

- **Stripe payment integration** — collect deposits or full payment at booking time
- **SMS confirmation to customer** — send the customer an SMS when their booking is confirmed
- **Customer booking status tracker** — shareable link for customers to track their booking status
- **Product / inventory catalog page** — showcase generators for sale with specs and pricing
- **PostgreSQL migration** — replace SQLite with a robust production database

---

## Customising the Site

| What to change | Where |
|---|---|
| Business name | Search `GenHome` in `index.html` and `admin.html` |
| Accent color | `--accent: #c8890a` in the `<style>` block of each HTML file |
| Contact details (address, phone, email, hours) | Contact section in `index.html` |
| About text & founding year | About section in `index.html` |
| Services descriptions | Services section in `index.html` |
| FAQ answers | FAQ section in `index.html` |
| Admin password | `ADMIN_PASSWORD` in `.env` |
