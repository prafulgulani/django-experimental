from django.conf import settings

def is_experiment_enabled(flag_name: str) -> bool:
    """
    Checks if a specific experimental feature flag is explicitly enabled
    in the user's settings.py.
    """
    # Experimental configuration dictionary
    flags = getattr(settings, "DJANGO_EXPERIMENTAL_FLAGS", {})    
    return bool(flags.get(flag_name, False))
