# Getting Started

This guide walks you through setting up HainNa for local development.

---

## Requirements

| Tool | Version | Install |
|---|---|---|
| Python | 3.12+ | [python.org](https://www.python.org/) |
| uv | latest | `pip install uv` or [astral.sh/uv](https://docs.astral.sh/uv/) |
| Git | any | [git-scm.com](https://git-scm.com/) |

---

## Installation

```bash
# 1. Clone
git clone https://github.com/komradkat/hainna.git
cd hainna

# 2. Install Python dependencies
uv sync

# 3. Create and configure .env
cp .env.example .env
```

At minimum, `.env` needs:

```env
DEBUG=True
SECRET_KEY=any-random-string-for-local-dev
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost

# CSRF (Required for some POST operations if using custom domains)
# CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

```bash
# 4. Apply database migrations
uv run python manage.py migrate

# 5. Create superuser
uv run python manage.py bootstrap_admin

# 6. (Optional) Seed routes for Leyte
uv run python manage.py seed_leyte

# 7. Start server
uv run python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) and log in with the credentials printed by `bootstrap_admin`.

---

## First-Time Configuration

### 1. Select Your Terminal

After login, click the **Active Station** badge in the top navigation bar to select which physical terminal this workstation belongs to (e.g., "Tacloban", "Ormoc"). This scopes the POS and Dispatch Board to only show trips for that terminal.

### 2. Add Routes

Go to **Fleet → Routes** and add inbound/outbound routes between terminals. Routes define origin → destination pairs and estimated travel times.

### 3. Add Vehicles & Drivers

Go to **Fleet → Vehicles** and **Fleet → Drivers** to register your fleet. For GPS tracking, add the Traccar Device ID to each vehicle (see [Traccar Integration](traccar-integration.md)).

### 4. Start a Trip

Go to **Booking → POS** to open a trip, issue tickets, and dispatch vehicles. The system auto-creates the return trip when a van arrives and completes its run.

---

## Project Structure

```
hainna/
├── apps/
│   ├── booking/      # Trips, tickets, POS, dispatch board
│   ├── core/         # Settings, base URLs, live tracking view
│   ├── fleet/        # Vehicles, drivers, routes, GPS service
│   └── users/        # Custom user model, authentication
├── docs/             # This documentation
├── logs/             # Application logs (auto-created)
├── static/           # Source static files (CSS, JS)
├── staticfiles/      # Collected static files (gitignored)
├── templates/        # Django HTML templates
├── manage.py
└── pyproject.toml
```

---

## Useful Management Commands

| Command | Description |
|---|---|
| `uv run python manage.py migrate` | Apply database migrations |
| `uv run python manage.py bootstrap_admin` | Create the default admin account |
| `uv run python manage.py seed_leyte` | Seed terminals and routes for Eastern Visayas |
| `uv run python manage.py collectstatic` | Collect static files for production |
| `uv run python manage.py check --deploy` | Run Django's production readiness checklist |
| `uv run python manage.py createsuperuser` | Create a custom superuser |
