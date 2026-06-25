import importlib
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def register_experimental_features():
    """
    Discover and initialize active experimental sub-packages.
    """
    if not settings.configured:
        return

    flags = getattr(settings, "DJANGO_EXPERIMENTAL_FLAGS", {})
    if not isinstance(flags, dict):
        raise ImproperlyConfigured(
            "DJANGO_EXPERIMENTAL_FLAGS must be a dictionary in settings.py"
        )

    # Iterate through runtime configuration flags to identify active features
    for flag_name, is_enabled in flags.items():
        if not is_enabled:
            continue

        if flag_name.startswith("ENABLE_"):
            experiment_name = flag_name.replace("ENABLE_", "").lower()
            sub_app_path = f"django.experimental.{experiment_name}"
            
            # Verify if the experiment package actually exists 
            try:
                spec = importlib.util.find_spec(sub_app_path)
                if spec is None:
                    raise ImportError
            except (ImportError, AttributeError, ValueError):
                raise ImproperlyConfigured(
                    f"Experimental flag '{flag_name}' is set to True, but the "
                    f"corresponding module '{sub_app_path}' does not exist."
                )

            # Verify that the user explicitly added the app to INSTALLED_APPS
            if sub_app_path not in settings.INSTALLED_APPS:
                raise ImproperlyConfigured(
                    f"The experiment '{flag_name}' is enabled, but you forgot to "
                    f"add '{sub_app_path}' to your INSTALLED_APPS in settings.py."
                )

            # Execute localized module configuration routines to switch AUTH_USER_MODEL
            try:
                config_module = importlib.import_module(f"{sub_app_path}.config")
                if hasattr(config_module, "modify_settings"):
                    config_module.modify_settings(settings)
            except ImportError:
                pass

register_experimental_features()