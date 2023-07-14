"""Base settings for the project."""
import os
from django.core.exceptions import ImproperlyConfigured

from division.core.settings import *  # noqa F401,F403
from division.core.settings_funcs import get_secret


for key in [
    "DIVISION_DB_NAME",
    "DIVISION_DB_USER",
    "DIVISION_DB_PASSWORD",
    "DIVISION_DB_HOST",
    "DIVISION_DB_PORT",
    "DIVISION_SECRET_KEY",
    "DIVISION_ALLOWED_HOSTS",
]:
    if not os.environ.get(key):
        raise ImproperlyConfigured(f"Required environment variable {key} is missing.") # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("DIVISION_SECRET_KEY", "django-insecure-0w5!cas22(uo_@sz7yi33zw0b@1jd*j9!fu8u=o8w0mr+1ax1iv")   # noqa

ALLOWED_HOSTS = os.getenv("DIVISION_ALLOWED_HOSTS", "*").split(" ")


DATABASES = {
    "default": {
        "NAME": os.getenv("DIVISION_DB_NAME", "division"),  # noqa  Database name
        "USER": os.getenv("DIVISION_DB_USER", ""),  # noqa  Database  username
        "PASSWORD": os.getenv("DIVISION_DB_PASSWORD", ""),  # noqa  Database password
        "HOST": os.getenv("DIVISION_DB_HOST", "localhost"),  # noqa  Database server
        "PORT": os.getenv("DIVISION_DB_PORT", ""),  # noqa   Database port (leave blank for default)
        "CONN_MAX_AGE": int(os.getenv("DIVISION_DB_TIMEOUT", "300")),  # noqa   Database timeout
        "ENGINE": os.getenv("DIVISION_DB_ENGINE", "django.db.backends.postgresql"), # noqa   Database driver "postgresql"
    }
}
