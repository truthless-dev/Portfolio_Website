from portfolio.settings.common import *  # noqa: F403


DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

SILENCED_SYSTEM_CHECKS = [
    "django_recaptcha.recaptcha_test_key_error",
]
