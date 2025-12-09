from pathlib import Path
import os

# --------------------------------------------------------
# Base directory
# --------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------
# Security
# --------------------------------------------------------
SECRET_KEY = 'django-insecure-your-secret-key'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# --------------------------------------------------------
# Installed Apps
# --------------------------------------------------------
INSTALLED_APPS = [
    # Admin Interface (must be above django.contrib.admin)
    'admin_interface',
    'colorfield',

    # Django built-in
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",

    # Local apps
    "inventory",
]

# --------------------------------------------------------
# Middleware
# --------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------------------------------
# URL & WSGI
# --------------------------------------------------------
ROOT_URLCONF = "inventory_backend.urls"
WSGI_APPLICATION = "inventory_backend.wsgi.application"

# --------------------------------------------------------
# Templates
# --------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --------------------------------------------------------
# Database
# --------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --------------------------------------------------------
# REST Framework
# --------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ]
}

# --------------------------------------------------------
# CORS
# --------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# --------------------------------------------------------
# Static & Media files
# --------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"     # For collectstatic

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------------
# Tailwind CSS (Optional)
# --------------------------------------------------------
# INSTALLED_APPS += ["tailwind", "theme"]
# TAILWIND_APP_NAME = "theme"
