import importlib
from django.core.exceptions import ImproperlyConfigured

AVAILABLE_EXPERIMENTS = {
    "ENABLE_NEWAUTH": "django.experimental.contrib.auth",
}

def register_experimental_features(settings):
    """
    Discover and initialize active experimental sub-packages.
    """
    if "DJANGO_EXPERIMENTAL_FLAGS" not in settings:
        return

    flags = settings.get("DJANGO_EXPERIMENTAL_FLAGS")
    if not isinstance(flags, dict):
        raise ImproperlyConfigured(
            "DJANGO_EXPERIMENTAL_FLAGS must be a dictionary in settings.py"
        )

    if not flags:
        return

    if "INSTALLED_APPS" not in settings:
        settings["INSTALLED_APPS"] = []
    installed_apps = settings["INSTALLED_APPS"]

    # Iterate through runtime configuration flags to identify active features
    for flag_name, is_enabled in flags.items():
        if flag_name not in AVAILABLE_EXPERIMENTS:
            raise ImproperlyConfigured(
                f"'{flag_name}' is not a recognized experimental feature flag. "
                f"Valid choices are: {', '.join(AVAILABLE_EXPERIMENTS.keys())}"
            )

        if not is_enabled:
            continue

        sub_app_path = AVAILABLE_EXPERIMENTS[flag_name]
        
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

        # Append active experiments to the installed applications registry
        if sub_app_path not in installed_apps:
            installed_apps.append(sub_app_path)

        # Execute localized module configuration routines to update settings
        try:
            config_module = importlib.import_module(f"{sub_app_path}.config")
            if hasattr(config_module, "modify_settings"):
                config_module.modify_settings(settings)
        except ImportError:
            pass