# django-experimental

[![PyPI](https://img.shields.io/pypi/v/django-experimental.svg)](https://pypi.org/project/django-experimental/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-experimental.svg)
![PyPI - License](https://img.shields.io/pypi/l/django-experimental.svg)

This is a third-party package built for testing how an experimental framework would work in Django. 

The goal of this project is to create a safe playground where new features can be built and tested using feature flags, 
without risking the stability of the main Django framework.

## Installation

```bash
pip install django-experimental

```

## Quick Setup

The setup uses dynamic injection at compilation time. This approach keeps `settings.py` clean by automatically adding required 
apps and experiment specific settings and prevents ghost logs when an experiment is turned off.

1. Add django.experimental to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    # ...
    "django.experimental",
]

```
2. Add the experimental flags dictionary and the registration hook at the bottom of your `settings.py`:

```python
# At the bottom of settings.py

DJANGO_EXPERIMENTAL_FLAGS = {
    "ENABLE_NEWAUTH": True,
}

from django.experimental import register_experimental_features
register_experimental_features(globals())

```

When `ENABLE_NEWAUTH` is set to `True`, the registration engine automatically:

* Adds `django.experimental.contrib.auth` into `INSTALLED_APPS`.
* Sets `AUTH_USER_MODEL = "experimental_auth.User"` (unless a custom user model is already configured).
* Adds `django.experimental.contrib.auth.backends.DualAuthenticationBackend` to `AUTHENTICATION_BACKENDS`.

When `ENABLE_NEWAUTH` is set to False, nothing is added and hence no ghost logs.

## Manual Setup

If you prefer to configure all settings explicitly without dynamic injection:

Add both the root package and the experimental module to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "django.experimental",
    "django.experimental.contrib.auth",
]

```

Configure the user model, authentication backends, and experimental flags in `settings.py`:

```python
AUTH_USER_MODEL = "experimental_auth.User"

AUTHENTICATION_BACKENDS = [
    # ...
    "django.experimental.contrib.auth.backends.DualAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

DJANGO_EXPERIMENTAL_FLAGS = {
    "ENABLE_NEWAUTH": True,
}

```

## Available Experiments

`NEWAUTH`: An updated User model for Django that includes a single full name field (replacing first/last name), 
unique email addresses, and supports logging in with a username or email.