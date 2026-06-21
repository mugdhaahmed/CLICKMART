# 🏗️ ClickMart — Architecture

This document describes how ClickMart is structured and how data flows through the system. For setup instructions see **[README.md](README.md)**.

---

## 1. High-Level Overview

ClickMart is a **decoupled** application: a stateless JSON API and a separate single-page client that talks to it over HTTP.

```
┌─────────────────────────┐         HTTP / JSON          ┌──────────────────────────┐
│   React SPA (Vite)      │  ───────────────────────────▶ │  Django REST Framework   │
│   localhost:5173        │   Bearer <access token>       │  API  /api/v1/           │
│                         │ ◀─────────────────────────── │  localhost:8000          │
│  - Axios + interceptors │        JSON responses         │                          │
│  - Context state        │                               │  - JWT auth              │
└─────────────────────────┘                               │  - App-per-domain        │
                                                          └────────────┬─────────────┘
                                                                       │
                                                                ┌──────▼───────┐
                                                                │ PostgreSQL   │
                                                                └──────────────┘
```

- **No server-side rendering** — Django serves only JSON (and media files in development); the React app owns all rendering and routing.
- **Authentication is token-based** — there are no server sessions for the SPA; the client holds JWTs in `localStorage`.
- **CORS** is restricted to the frontend origin (`http://localhost:5173`).

---

## 2. Backend Architecture (Django REST Framework)

The backend follows Django's **app-per-domain** convention. Each app owns its models, serializers, and views; a single central app wires their URLs together.

### 2.1 Project configuration — `clickmart_main/`

- **`settings.py`** — installed apps, PostgreSQL connection (via `python-decouple` env vars), DRF defaults, SimpleJWT token lifetimes, CORS, SMTP email, custom user model, and media handling.
- **`urls.py`** — mounts the Django admin and includes `api.urls` under `api/v1/`. In `DEBUG` mode it also serves uploaded media.
- **`wsgi.py` / `asgi.py`** — server entry points (Gunicorn uses WSGI in Docker).

### 2.2 URL routing — `api/`

The `api` app contains **no models or business logic**. Its single job is [`api/urls.py`](backend/api/urls.py), which imports views from every domain app and exposes the full API surface under `/api/v1/`. JWT login/refresh endpoints (from SimpleJWT) are registered here too.

### 2.3 Domain apps

| App | Models | Responsibility |
|-----|--------|----------------|
| **users** | `User` (extends `AbstractUser`, **email is the login field**) | Registration & profile |
| **products** | `Category`, `Product` | Read-only catalog APIs |
| **carts** | `Cart`, `CartItem` | Per-user persistent cart with computed totals |
| **orders** | `Order`, `OrderItem` | Checkout, order snapshots, history, email |

#### users
- `User` sets `USERNAME_FIELD = "email"`, so authentication is by email. Registered as `AUTH_USER_MODEL`.
- `RegisterView` (open) creates users via `create_user`; `ProfileView` (authenticated) returns the current user.

#### products
- Read-only generic views (`ListAPIView` / `RetrieveAPIView`). Only `product_is_active=True` products are exposed.
- `Product` carries price, stock, image, and a per-product `product_tax_percentage` used in cart math.

#### carts
- `Cart` has a **one-to-one** relationship with the user — each user has exactly one cart, created on demand (`get_or_create`).
- Totals are **computed properties** on the model, not stored columns:
  - `subtotal` = Σ (price × quantity)
  - `tax_amount` = Σ (price × quantity × tax%)
  - `grand_total` = subtotal + tax
- `CartItem` links a cart to a product with a quantity (`related_name="cart_items"`).

#### orders
- `Order` stores a **snapshot** of monetary totals and shipping details at purchase time; `OrderItem` stores a per-line snapshot (product, quantity, unit price, line total) so historical orders are unaffected by later price/stock changes.
- `Order.user` and `OrderItem.product` use `on_delete=PROTECT` to prevent destroying historical records.
- `orders/utils.py` sends a confirmation email after a successful order.

### 2.4 Data Model

```
User (1) ──── (1) Cart (1) ──── (N) CartItem (N) ──── (1) Product (N) ──── (1) Category
  │                                                          │
  │ (1)                                                      │ (N)
  │                                                          │
  └──── (N) Order (1) ──── (N) OrderItem (N) ────────────────┘
```

- One user → one cart → many cart items.
- One user → many orders → many order items.
- Products belong to a category; cart items and order items reference products.

---

## 3. Request & Authentication Flow

### 3.1 Login

```
Client                         API
  │  POST /api/v1/token/         │
  │  { email, password }         │
  │ ───────────────────────────▶ │  SimpleJWT validates credentials
  │ ◀─────────────────────────── │  { access, refresh }
  │  store both in localStorage  │
```

### 3.2 Authenticated request + automatic refresh

The frontend's `useAxios` hook installs two interceptors on the shared Axios instance:

1. **Request interceptor** — attaches `Authorization: Bearer <accessToken>` to every outgoing request.
2. **Response interceptor** — on a `401`, it performs a **single-flight** token refresh (`POST /token/refresh/`), retries the original request with the new token, and — if the refresh fails — clears tokens and redirects home.

```
Client                                    API
  │  GET /cart/  (expired access token)     │
  │ ──────────────────────────────────────▶ │  401 Unauthorized
  │ ◀────────────────────────────────────── │
  │  POST /token/refresh/ { refresh }        │
  │ ──────────────────────────────────────▶ │  { access }
  │ ◀────────────────────────────────────── │
  │  retry GET /cart/  (new access token)    │
  │ ──────────────────────────────────────▶ │  200 OK
```

"Single-flight" means concurrent 401s share **one** refresh promise instead of triggering many refresh calls.

### 3.3 Checkout flow

```
Cart page ──▶ Checkout (Step 1: shipping) ──▶ Checkout (Step 2: review)
                                                      │
                                                      ▼
                                         POST /orders/place/
                                         { shippingAddress }
                                                      │
                          ┌───────────────────────────┴───────────────────────────┐
                          ▼                                                         ▼
              create Order + OrderItem snapshots                        send confirmation email
                          │
                          ▼
                  clear the cart items
                          │
                          ▼
            redirect to /order/success/:id
```

---

## 4. Frontend Architecture (React + Vite)

### 4.1 Composition

`main.jsx` wraps the app in two context providers:

```
<AuthProvider>        ← holds JWT tokens (seeded from localStorage)
  <CartProvider>      ← holds cart state via useReducer
    <App />           ← Router + routes
  </CartProvider>
</AuthProvider>
```

### 4.2 State management

- **Auth state** — `AuthProvider` keeps `{ accessToken, refreshToken }`; consumed through the `useAuth()` hook. Tokens are mirrored in `localStorage` for persistence across reloads.
- **Cart state** — `CartProvider` uses a `useReducer` store (`items`, `subtotal`, `total`, `itemCount`, `loading`) with actions `START_LOADING`, `SET_CART`, `STOP_LOADING`; consumed through `useCart()`.

### 4.3 API layer

- `src/api/index.js` — a base Axios instance configured with `VITE_SERVER_BASE_URL`. Used directly for **public** reads (e.g. product listing).
- `src/hooks/useAxios.js` — returns the same instance but with the auth/refresh interceptors attached; used for **authenticated** calls.

### 4.4 Routing

| Path | Page | Access |
|------|------|--------|
| `/` | Home (Hero + Products) | Public |
| `/product/:id` | Product detail | Public |
| `/cart` | Shopping cart | Public* |
| `/checkout` | Two-step checkout | Public* |
| `/login`, `/signup` | Auth forms | Public |
| `/order/success/:id` | Confirmation page | Public |
| `/dashboard` | Dashboard shell (Sidebar + Outlet) | **Protected** |
| `/dashboard` (index) | Dashboard home | **Protected** |
| `/dashboard/profile` | Profile settings | **Protected** |
| `/dashboard/orders` | Order history + detail modal | **Protected** |

\* Cart/checkout pages render for anyone, but the underlying cart API calls require authentication; `PrivateRoute` gates the dashboard by checking for an access token.

### 4.5 Key components

- **Navbar** — brand, cart badge (driven by `itemCount`), profile dropdown, and logout (clears tokens + cart).
- **OrderDetail** — Bootstrap modal that fetches `/orders/:id` and renders items, totals, and delivery info.
- **QuantitySelector** — reusable +/- control used in cart and product detail.
- **PrivateRoute** — wraps protected routes, redirecting to `/login` when no token is present.

---

## 5. Deployment

The project ships with a multi-container setup (`docker-compose.yml`):

| Service | Image / Build | Notes |
|---------|---------------|-------|
| **db** | `postgres:16-alpine` | Data persisted to the `postgres_data` named volume |
| **backend** | `./backend/Dockerfile` (Python 3.12 + Gunicorn) | Runs `collectstatic` + `migrate` on startup; serves on `:8000` |
| **frontend** | `./frontend/Dockerfile` (multi-stage: Node build → Nginx) | Static build served by Nginx on `:5173` |

The frontend Docker build bakes the API URL in at build time via the `VITE_SERVER_BASE_URL` build argument, since Vite inlines env vars during the build.

---

## 6. Design Notes & Conventions

- **Totals are computed, never trusted from the client.** Cart subtotal/tax/grand total are derived server-side from current product prices; the order then snapshots these values.
- **Snapshots protect history.** Orders copy prices and quantities at purchase time and use `PROTECT` deletes so historical orders remain accurate.
- **One cart per user**, created lazily — the client never has to manage cart creation.
- **Stateless API** — all client identity travels in the JWT; the server keeps no SPA session.
