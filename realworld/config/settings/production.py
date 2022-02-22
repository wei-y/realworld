# flake8: noqa

import dj_database_url

from .base import *

DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
MIDDLEWARE.insert(5, "django.middleware.gzip.GZipMiddleware")


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # 1 year

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True


# ==============================================================================
# WHITENOISE SETTINGS
# ==============================================================================

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
