import os

from portfolio.settings.common import *  # noqa: F403


DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "712.235.50.46",
    ".tylerchristie.dev",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DJANGO_DB_NAME"],
        "USER": os.environ["DJANGO_DB_USER"],
        "PASSWORD": os.environ["DJANGO_DB_PASSWORD"],
        "HOST": "127.0.0.1",
        "PORT": "",
    }
}
