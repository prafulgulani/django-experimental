from django.core.exceptions import ImproperlyConfigured

def modify_settings(settings):
    user_model_setting = getattr(settings, "AUTH_USER_MODEL", "auth.User")
    allowed_states = ["auth.User", "newauth.NewUser"]

    if user_model_setting not in allowed_states:
        raise ImproperlyConfigured(
            f"Conflict detected: The 'newauth' experiment is active, but your "
            f"settings.py explicitly overrides AUTH_USER_MODEL to '{user_model_setting}'."
        )

    settings.AUTH_USER_MODEL = "newauth.NewUser"
    
    settings.AUTHENTICATION_BACKENDS = [
        "django.experimental.newauth.backends.DualAuthenticationBackend",
    ]
