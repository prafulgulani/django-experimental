from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ExperimentalConfig(AppConfig):
    """
    Application configuration for the Django experimental features registry.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "django.experimental"
    verbose_name = _("Django Experimental Features")

    def ready(self):
        """
        Scan active configuration flags at runtime to log initialized modules.
        """
        flags = getattr(settings, "DJANGO_EXPERIMENTAL_FLAGS", {})
        if not isinstance(flags, dict):
            return

        for flag_name, is_enabled in flags.items():
            if is_enabled and flag_name.startswith("ENABLE_"):
                experiment_name = flag_name.replace("ENABLE_", "").lower()
                print(f"[Django Experimental] Active and monitoring '{experiment_name}' environment.")