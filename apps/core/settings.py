"""
Django settings for HainNa project.
"""

import os
import environ
import logging
from pathlib import Path

import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False),
    PRODUCTION=(bool, False),
    SECRET_KEY=(str, None),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    SECURE_SSL_REDIRECT=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
    SECURE_HSTS_SECONDS=(int, 0),
    USE_X_FORWARDED_HOST=(bool, True),
)

# Reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ── Core ────────────────────────────────────────────────────────────────────

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
PRODUCTION = env('PRODUCTION', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])

# ── Applications ─────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'fleet.apps.FleetConfig',
    'booking.apps.BookingConfig',
]

# ── Middleware ────────────────────────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # Serve static files efficiently
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ── Database ──────────────────────────────────────────────────────────────────
# For production: set DATABASE_URL=postgres://user:pass@host:5432/dbname

DATABASES = {
    'default': env.db(),
}
DATABASES['default']['CONN_MAX_AGE'] = 60  # Connection pooling (seconds)

# ── Password Validation ───────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ──────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# ── Static & Media Files ──────────────────────────────────────────────────────

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Default primary key ───────────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Authentication ────────────────────────────────────────────────────────────

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'loading_screen'
LOGOUT_REDIRECT_URL = 'login'

# Sessions — expire after 8 hours or on browser close (important for shared cashier terminals)
SESSION_COOKIE_AGE = 28800       # 8 hours in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ── Security Headers ──────────────────────────────────────────────────────────

# Core Security
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# SSL & Redirects (defaults are based on PRODUCTION flag if not specified in .env)
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', default=PRODUCTION)
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', default=PRODUCTION)
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', default=PRODUCTION)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000 if PRODUCTION else 0)

# Proxy Headers (Required for HTTPS detection behind a load balancer/proxy)
SECURE_PROXY_SSL_HEADER = env.tuple('SECURE_PROXY_SSL_HEADER', default=('HTTP_X_FORWARDED_PROTO', 'https'))
USE_X_FORWARDED_HOST = env.bool('USE_X_FORWARDED_HOST', default=True)

if PRODUCTION:
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'

# ── Traccar GPS Integration ───────────────────────────────────────────────────

TRACCAR_URL = env('TRACCAR_URL', default='http://localhost:8082')
TRACCAR_USER = env('TRACCAR_USER', default='admin')
TRACCAR_PASSWORD = env('TRACCAR_PASSWORD', default='admin')

# ── Logging ───────────────────────────────────────────────────────────────────

LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'hainna.log',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}