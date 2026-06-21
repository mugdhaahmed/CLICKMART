# 🛒 ClickMart

A full-stack e-commerce application built with a **Django REST Framework** API backend and a **React (Vite)** single-page frontend. ClickMart supports product browsing, a persistent server-side cart, JWT-based authentication, order placement with email confirmation, and an order history dashboard.

---

## ✨ Features

- **Product catalog** — browse active products and categories, view product details with live stock status.
- **Authentication** — register, log in, and stay signed in via JWT access/refresh tokens with automatic token refresh.
- **Shopping cart** — one cart per user, persisted in the database; add items, increase/decrease quantity (stock-aware), and remove items.
- **Checkout & orders** — two-step checkout (shipping → review), order placement that snapshots cart contents, and an automatic confirmation email.
- **Order history** — dashboard listing past orders with a detail modal showing items, totals, and delivery info.
- **Admin panel** — Django admin for managing categories, products, carts, and orders (with inline order items).

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 6.0.5, Django REST Framework 3.17, SimpleJWT, PostgreSQL (psycopg2), Pillow, python-decouple, django-cors-headers |
| **Frontend** | React 19, Vite 7, React Router 7, Axios, Bootstrap 5, Bootstrap Icons, Lucide React, React Toastify |
| **Auth** | JWT (access + refresh tokens) |
| **Deployment** | Docker, Docker Compose, Nginx (frontend), Gunicorn (backend) |

---

## 📁 Project Structure

```
CLICKMART/
├── backend/                  # Django REST API
│   ├── clickmart_main/       # Project config (settings, urls, wsgi/asgi)
│   ├── api/                  # Central API URL router (api/v1/)
│   ├── users/                # Custom user model, registration, profile
│   ├── products/             # Category & Product models + read APIs
│   ├── carts/                # Cart & CartItem models + cart APIs
│   ├── orders/              # Order & OrderItem models, checkout, email
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # React + Vite SPA
│   ├── src/
│   │   ├── api/              # Axios base instance
│   │   ├── hooks/            # useAuth, useAxios (token refresh interceptor)
│   │   ├── Provider/         # Auth & Cart context providers
│   │   ├── context/          # Auth & Cart contexts
│   │   ├── components/        # Navbar, Footer, Sidebar, modals, etc.
│   │   └── pages/            # Home, Products, Cart, Checkout, Orders, ...
│   └── Dockerfile
├── docker-compose.yml
├── ARCHITECTURE.md          # Detailed architecture documentation
└── LICENSE.md
```

See **[ARCHITECTURE.md](ARCHITECTURE.md)** for a deeper explanation of how the pieces fit together.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 14+

### 1. Backend

```bash
cd backend

# create & activate a virtual environment
python -m venv env
source env/Scripts/activate      # Windows (Git Bash)
# source env/bin/activate        # macOS / Linux

pip install -r requirements.txt

# create your .env (see "Environment Variables" below)
python manage.py migrate
python manage.py createsuperuser   # optional, for admin access
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/v1/`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## 🔐 Environment Variables

Sample templates are included — copy each and fill in your own values:

```bash
cp backend/.env.sample            backend/.env             # local development
cp backend/.env.docker.sample     backend/.env.docker      # backend container
cp backend/.env.production.sample backend/.env.production   # postgres container
```

### `backend/.env`

```env
SECRET_KEY='your-django-secret-key'
DEBUG=True

DB_NAME='clickmart'
DB_USER='postgres'
DB_PASS='your-db-password'
DB_HOST='localhost'
DB_PORT='5432'

ACCESS_TOKEN_EXPIRY=15          # minutes
REFRESH_TOKEN_EXPIRY=3          # days

EMAIL_HOST_USER='you@gmail.com'
EMAIL_HOST_PASSWORD='your-app-password'
```

### `frontend/.env`

```env
VITE_SERVER_BASE_URL=http://127.0.0.1:8000/api/v1
```

> **Note:** the backend reads the database password from `DB_PASS`. Keep this name consistent across `.env` and `.env.docker`.

---

## 🐳 Running with Docker

```bash
docker compose up --build
```

This starts three services:

| Service | Description | Port |
|---------|-------------|------|
| `db` | PostgreSQL 16 | 5432 (internal) |
| `backend` | Django + Gunicorn (runs migrate & collectstatic on start) | 8000 |
| `frontend` | Production build served by Nginx | 5173 |

Environment is supplied via `backend/.env.docker` (backend) and `backend/.env.production` (database).

---

## 📡 API Endpoints

Base path: `/api/v1/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/register/` | — | Register a new user |
| `POST` | `/token/` | — | Obtain access + refresh tokens (login) |
| `POST` | `/token/refresh/` | — | Refresh an access token |
| `GET`  | `/profile/` | ✅ | Current user's profile |
| `GET`  | `/products/` | — | List active products |
| `GET`  | `/products/<id>/` | — | Product detail |
| `GET`  | `/category/` | — | List categories |
| `GET`  | `/cart/` | ✅ | Get (or create) the user's cart |
| `POST` | `/cart/add/` | ✅ | Add a product to the cart |
| `PATCH` | `/cart/items/<id>/` | ✅ | Increase/decrease item quantity |
| `DELETE` | `/cart/items/<id>/` | ✅ | Remove an item from the cart |
| `POST` | `/orders/place/` | ✅ | Place an order from the current cart |
| `GET`  | `/orders/` | ✅ | List the user's orders |
| `GET`  | `/orders/<id>` | ✅ | Order detail (with items) |

---

## 📝 License

This project is **not** open source. You may copy or use it **only with the author's explicit permission**. See **[LICENSE.md](LICENSE.md)**.

---

## 👤 Author

**Golam Ahmed Mugdha** — golamahmedmugdha@gmail.com
