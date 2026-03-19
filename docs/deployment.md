# Production Deployment Guide

This guide covers deploying HainNa on a Linux VPS with PostgreSQL, Gunicorn, and Nginx.

---

## 1. Prerequisites

- Ubuntu 22.04+ VPS
- A domain name pointing to your server's IP
- Python 3.12+, `uv`, Git installed

---

## 2. PostgreSQL Setup

```bash
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql

CREATE DATABASE hainna;
CREATE USER hainna_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE hainna TO hainna_user;
\q
```

---

## 3. Clone & Configure

```bash
git clone https://github.com/komradkat/hainna.git /opt/hainna
cd /opt/hainna

uv sync

cp .env.example .env
nano .env
```

**Production `.env` settings:**

```env
DEBUG=False
PRODUCTION=True
SECRET_KEY=<run: openssl rand -hex 50>
DATABASE_URL=postgres://hainna_user:strong_password_here@localhost:5432/hainna
ALLOWED_HOSTS=hainna.yourdomain.com
TRACCAR_URL=http://localhost:8082
TRACCAR_USER=admin
TRACCAR_PASSWORD=your_traccar_password
```

---

## 4. Migrate & Collect Static Files

```bash
uv run python manage.py migrate
uv run python manage.py collectstatic --no-input
uv run python manage.py bootstrap_admin
```

---

## 5. Gunicorn Service

Create `/etc/systemd/system/hainna.service`:

```ini
[Unit]
Description=HainNa Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/hainna
ExecStart=/opt/hainna/.venv/bin/gunicorn \
  core.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 4 \
  --timeout 120 \
  --access-logfile /opt/hainna/logs/gunicorn-access.log \
  --error-logfile /opt/hainna/logs/gunicorn-error.log
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable hainna
sudo systemctl start hainna
```

---

## 6. Nginx Config

Install Nginx and create `/etc/nginx/sites-available/hainna`:

```nginx
server {
    listen 80;
    server_name hainna.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name hainna.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/hainna.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hainna.yourdomain.com/privkey.pem;

    location /static/ {
        alias /opt/hainna/staticfiles/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location /media/ {
        alias /opt/hainna/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/hainna /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 7. SSL — Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d hainna.yourdomain.com
```

Certbot auto-renews. Verify with `sudo certbot renew --dry-run`.

---

## 8. Verify

```bash
# Check Django
uv run python manage.py check --deploy

# Check service
sudo systemctl status hainna

# Check logs
tail -f /opt/hainna/logs/hainna.log
tail -f /opt/hainna/logs/gunicorn-error.log
```

---

## Deployment via Docker (Simplified)

For a modern, containerized deployment:

1. **Install Docker & Docker Compose** on your VPS.
2. **Clone the repo** and copy `.env.example` to `.env`.
3. Set `PRODUCTION=True` and configure `DATABASE_URL` in `.env`.
4. Run everything:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```
5. Run initialization:
   ```bash
   docker-compose exec app python manage.py migrate
   docker-compose exec app python manage.py collectstatic --no-input
   docker-compose exec app python manage.py bootstrap_admin
   ```

---

## Updating

```bash
cd /opt/hainna
git pull
uv sync
uv run python manage.py migrate
uv run python manage.py collectstatic --no-input
sudo systemctl restart hainna
```
