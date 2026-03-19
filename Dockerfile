# Use a slim Python 3.12 image
FROM python:3.12-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency files first to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install dependencies into the system site-packages (no venv needed in container)
RUN uv sync --frozen --no-cache --no-dev

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=core.settings
ENV PYTHONPATH="/app/apps"
ENV PATH="/app/.venv/bin:$PATH"

# New Security Environment Variables (Defaults)
ENV CSRF_TRUSTED_ORIGINS=""
ENV SECURE_SSL_REDIRECT=False
ENV SESSION_COOKIE_SECURE=False
ENV CSRF_COOKIE_SECURE=False
ENV SECURE_HSTS_SECONDS=0

# Collect static files (requires standard dummy env vars if they aren't provided)
# Note: In a real deploy, you'd provide real env vars or skip this until runtime.
RUN SECRET_KEY=build-time-only-key uv run python manage.py collectstatic --no-input

# Expose port
EXPOSE 8000

# Default command to run gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
