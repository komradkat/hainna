# HainNa — Fleet & Booking Management System

> Terminal-aware fleet dispatch and passenger booking platform for Philippine provincial bus/van operations.

[![Django](https://img.shields.io/badge/Django-6.0-green)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

---

## Features

| Module | Description |
|---|---|
| 🚐 **Fleet Management** | Vehicles, drivers, routes, service logs, fuel monitoring |
| 🎫 **Booking & Dispatch** | POS-style ticket issuance, trip queue management, FIFO dispatch |
| 📺 **Public TV Board** | Large-font departure/arrival board for terminal displays |
| 🗺️ **Live Tracking** | Real-time GPS map via Traccar integration (5s polling) |
| 🏢 **Terminal Awareness** | Each cashier session is scoped to a physical terminal |
| 👥 **User Management** | Role-based access, password policy enforcement |
| 📊 **Analytics** | Trip statistics and fleet utilisation (in progress) |

---

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- (Optional) PostgreSQL for production

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/komradkat/hainna.git
cd hainna

# 2. Install dependencies
uv sync

# 3. Set up environment
cp .env.example .env
# Edit .env — at minimum set SECRET_KEY and DATABASE_URL

# 4. Run migrations
uv run python manage.py migrate

# 5. Create an admin user
uv run python manage.py bootstrap_admin

# 6. (Optional) Seed Philippine routes
uv run python manage.py seed_leyte

# 7. Start development server
uv run python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and log in.

### Using Docker (Recommended for Local & Prod)

```bash
# 1. Start all services (Django + Postgres + Traccar)
docker-compose up -d

# 2. Run migrations
docker-compose exec app python manage.py migrate

# 3. Create admin
docker-compose exec app python manage.py bootstrap_admin
```

The app will be at [http://localhost:8000](http://localhost:8000), Traccar at [http://localhost:8082](http://localhost:8082).

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ | Django secret key. Generate: `openssl rand -hex 50` |
| `DEBUG` | ✅ | `True` for dev, `False` for production |
| `PRODUCTION` | — | Set `True` in production to activate HTTPS security headers |
| `DATABASE_URL` | ✅ | `sqlite:///db.sqlite3` (dev) or `postgres://...` (prod) |
| `ALLOWED_HOSTS` | ✅ | Comma-separated hostnames, e.g. `hainna.yourdomain.com` |
| `TRACCAR_URL` | — | Traccar server URL, e.g. `http://localhost:8082` |
| `TRACCAR_USER` | — | Traccar admin username |
| `TRACCAR_PASSWORD` | — | Traccar admin password |

See individual docs in [`/docs`](docs/) for feature-specific configuration.

---

## Documentation

| Doc | Description |
|---|---|
| [Getting Started](docs/getting-started.md) | Full setup walkthrough |
| [Traccar GPS Integration](docs/traccar-integration.md) | Connecting vehicles to GPS tracking |
| [Terminal Setup](docs/terminal-setup.md) | Configuring physical dispatch terminals |
| [Production Deployment](docs/deployment.md) | Gunicorn, Nginx, PostgreSQL, SSL |
| [Architecture Overview](docs/architecture.md) | App structure, data flow, key models |

---

## Tech Stack

- **Backend**: Django 6.0, Python 3.12
- **Frontend**: HTMX, Alpine.js, TailwindCSS / DaisyUI
- **Map**: Leaflet.js + CartoDB tiles
- **GPS**: Traccar (self-hosted)
- **Static Files**: WhiteNoise
- **Production Server**: Gunicorn

---

## Production Checklist

- [ ] Set `SECRET_KEY` to a randomly generated value
- [ ] Set `DEBUG=False` and `PRODUCTION=True`  
- [ ] Use PostgreSQL (`DATABASE_URL=postgres://...`)
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Run `uv run python manage.py collectstatic`
- [ ] Start with Gunicorn (see [deployment guide](docs/deployment.md))
- [ ] Configure SSL via Let's Encrypt / Certbot

---

## License

MIT — see [LICENSE](LICENSE).
