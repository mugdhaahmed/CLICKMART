# 🚀 Deploying ClickMart (100% free)

A step-by-step guide to deploy ClickMart using only free, no-credit-card services.

## Stack

| Component | Service | Free? |
|-----------|---------|-------|
| Backend (Django API) | Render Web Service | ✅ |
| Frontend (React build) | Render Static Site | ✅ |
| Database (PostgreSQL) | Neon | ✅ (persistent) |
| Media (product images) | Cloudinary | ✅ |
| Keep-awake pinger | UptimeRobot | ✅ |

The repo includes a [`render.yaml`](render.yaml) Blueprint that creates both Render services at once.

> **Heads-up:** the free backend sleeps after ~15 min idle (first request then takes ~30–60s). The pinger (Step 6) keeps it warm.

---

## Step 1 — Database (Neon)

1. Sign up at **[neon.tech](https://neon.tech)** (GitHub login, no card).
2. Create a project → it gives you a **connection string**.
3. Use the **Pooled connection** string (recommended for serverless). It looks like:
   ```
   postgresql://USER:PASSWORD@ep-xxxx-pooler.REGION.aws.neon.tech/DBNAME?sslmode=require
   ```
4. Save it — this is your **`DATABASE_URL`**.

## Step 2 — Media storage (Cloudinary)

1. Sign up at **[cloudinary.com](https://cloudinary.com)** (no card).
2. On the dashboard, copy the **API environment variable**:
   ```
   CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
   ```
3. Save the value after `CLOUDINARY_URL=` — this is your **`CLOUDINARY_URL`**.

## Step 3 — Email (Gmail App Password)

You should already have this from rotating secrets. If not: Google Account → Security → 2-Step Verification → **App passwords** → create one (16 chars, remove spaces). Keep your Gmail address (`EMAIL_HOST_USER`) and the app password (`EMAIL_HOST_PASSWORD`).

---

## Step 4 — Deploy on Render (Blueprint)

1. Make sure `render.yaml` is committed and pushed to GitHub.
2. **[dashboard.render.com](https://dashboard.render.com)** → **New** → **Blueprint** → connect the `CLICKMART` repo.
3. Render reads `render.yaml` and creates **clickmart-backend** + **clickmart-frontend**, prompting for the `sync: false` values. Fill them in:

**Backend env vars**
| Key | Value |
|-----|-------|
| `DATABASE_URL` | (from Step 1) |
| `CLOUDINARY_URL` | (from Step 2) |
| `EMAIL_HOST_USER` | your Gmail address |
| `EMAIL_HOST_PASSWORD` | your Gmail app password |
| `CORS_ALLOWED_ORIGINS` | `https://clickmart-frontend.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://clickmart-frontend.onrender.com` |

**Frontend env var**
| Key | Value |
|-----|-------|
| `VITE_SERVER_BASE_URL` | `https://clickmart-backend.onrender.com/api/v1` |

> Render service URLs are `https://<service-name>.onrender.com`. The names above assume `clickmart-backend` / `clickmart-frontend` are available — if Render appended a suffix because a name was taken, use the actual URLs shown in the dashboard and update these three values accordingly.

4. **Apply**. The backend build runs `pip install`, `collectstatic`, and **`migrate`** automatically; the frontend builds and deploys to the CDN.

`SECRET_KEY`, `DEBUG=False`, `PYTHON_VERSION`, and the token-expiry vars are set automatically by `render.yaml` — you don't enter those.

## Step 5 — Create an admin user

Once the backend is live: backend service → **Shell** tab → run:
```bash
python manage.py createsuperuser
```
Then log in at `https://clickmart-backend.onrender.com/admin/` to add categories/products (images upload to Cloudinary).

## Step 6 — Keep the backend awake (pinger)

1. Sign up at **[uptimerobot.com](https://uptimerobot.com)** (free).
2. Add a **HTTP(s)** monitor:
   - URL: `https://clickmart-backend.onrender.com/api/v1/health/`
   - Interval: **5 minutes**
3. This pings the lightweight health endpoint so the service rarely sleeps during the day.

---

## ✅ Verify

- Backend health: open `https://clickmart-backend.onrender.com/api/v1/health/` → `{"status":"ok"}`
- Products API: `https://clickmart-backend.onrender.com/api/v1/products/`
- Frontend: `https://clickmart-frontend.onrender.com` → loads, products show, login/cart/checkout work

## 🔁 Future deploys

Both services auto-deploy on every push to `main`. Just:
```bash
git push origin main
```

## 🧠 Notes & gotchas

- **First load after idle is slow** (~30–60s) on free tier — the pinger mitigates this.
- **Neon** also auto-suspends; the first query wakes it (~0.5s).
- **Media** only persists because of Cloudinary — never rely on the server filesystem for uploads on Render.
- **Migrations** run during the backend build. For data migrations or a fresh DB, that's automatic; to run manually use the backend **Shell**.
- **Custom domain** (optional, free): add it in Render, then add the domain to `ALLOWED_HOSTS`/`CORS_ALLOWED_ORIGINS`/`CSRF_TRUSTED_ORIGINS`.
- The `backend/Dockerfile`, `frontend/Dockerfile`, and `docker-compose.yml` are **not used** by this Render deploy — they remain for local Docker / a VPS deploy.
