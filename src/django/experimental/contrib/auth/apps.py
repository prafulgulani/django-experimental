from django.apps import AppConfig
from django.core import checks
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.apps import apps
from django.utils.translation import gettext_lazy as _


def check_experimental_user_subclass(app_configs, **kwargs):
    """
    Validates that the custom AUTH_USER_MODEL properly inherits from the
    experimental base configuration class after the app registry populates.
    """
    errors = []
    try:
        custom_user_model = apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)
    except (ValueError, LookupError):
        return [
            checks.Error(
                f"AUTH_USER_MODEL points to an invalid model string: '{settings.AUTH_USER_MODEL}'.",
                id="experimental_auth.E001",
            )
        ]

    from .models import AbstractUser
    
    if not issubclass(custom_user_model, AbstractUser):
        errors.append(
            checks.Error(
                f"Conflict detected: The active experiment 'ENABLE_NEWAUTH' requires that "
                f"'{settings.AUTH_USER_MODEL}' inherits from 'django.experimental.contrib.auth.models.AbstractUser'.",
                id="experimental_auth.E002",
            )
        )
    return errors


class ExperimentalAuthConfig(AppConfig):
    name = "django.experimental.contrib.auth"
    verbose_name = _("Experimental Auth")
    label = "experimental_auth"
    
    def ready(self):
        """
        Register validation hooks into the framework check engine.
        """
        checks.register(check_experimental_user_subclass, checks.Tags.models)