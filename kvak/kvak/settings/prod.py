from .base import *

DEBUG = bool(os.getenv("DJANGO_DEBUG", False))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "<TODO>")

_DJANGO_DOMAIN = os.getenv("DJANGO_DOMAIN", "localhost")
ALLOWED_HOSTS = [_DJANGO_DOMAIN]
CSRF_TRUSTED_ORIGINS = [f"https://{_DJANGO_DOMAIN}"]
WAGTAILADMIN_BASE_URL = f"https://{_DJANGO_DOMAIN}"

STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT", os.path.join(BASE_DIR, "static"))
STATIC_URL = os.getenv("DJANGO_STATIC_URL_BASE", "/static/")

# Email settings
EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.filebased.EmailBackend",
)
EMAIL_FILE_PATH = os.getenv("DJANGO_EMAIL_FILE_PATH", "/tmp/emails")
EMAIL_USE_TLS = bool(os.getenv("DJANGO_EMAIL_USE_TLS", ""))
EMAIL_USE_SSL = bool(os.getenv("DJANGO_EMAIL_USE_SSL", ""))
EMAIL_HOST = os.getenv("DJANGO_EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("DJANGO_EMAIL_PORT", None) or "0")
EMAIL_HOST_USER = os.getenv("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("DJANGO_EMAIL_HOST_PASSWORD", "")
FROM_EMAIL = os.getenv("DJANGO_FROM_EMAIL", "")
REPLY_TO_EMAIL = os.getenv("DJANGO_REPLY_TO_EMAIL", "")
DEFAULT_FROM_EMAIL = FROM_EMAIL
