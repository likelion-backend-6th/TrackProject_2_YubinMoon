import os
from .base import *

DJANGO_ALLOWED_HOST = os.getenv("DJANGO_ALLOWED_HOST", "localhost")

ALLOWED_HOSTS = [DJANGO_ALLOWED_HOST]

CSRF_TRUSTED_ORIGINS = [f"http://{DJANGO_ALLOWED_HOST}"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "OPTIONS": {"options": "-c search_path=sample,public"},
    }
}
