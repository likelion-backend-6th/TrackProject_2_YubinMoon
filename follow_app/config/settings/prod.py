import os
from .base import *

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# static 파일 서비스를 위해
# 추후 nginx를 추가해 줘야 할 듯 하다.
# 쿠버네티스로 넘어가면 괜찮겠지만
DEBUG = True

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOST", "localhost")]

CSRF_TRUSTED_ORIGINS = [f"http://{os.getenv('ALLOWED_HOST', 'localhost')}"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "OPTIONS": {"options": "-c search_path=sample,public"},
    }
}
