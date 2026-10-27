from tests.settings import *

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.experimental",
    "django.experimental.contrib.auth",
    "auth_tests",
]

AUTH_USER_MODEL = "experimental_auth.User"

AUTHENTICATION_BACKENDS = [
    "django.experimental.contrib.auth.backends.DualAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

DJANGO_EXPERIMENTAL_FLAGS = {
    "ENABLE_NEWAUTH": True,
}