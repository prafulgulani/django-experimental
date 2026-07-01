def modify_settings(settings):
    current_user_model = settings.get("AUTH_USER_MODEL", "auth.User")

    if current_user_model == "auth.User":
        settings["AUTH_USER_MODEL"] = "experimental_auth.User"
    
    backends = settings.get("AUTHENTICATION_BACKENDS", ["django.contrib.auth.backends.ModelBackend"])
    backends = list(backends)
        
    experimental_backend = "django.experimental.contrib.auth.backends.DualAuthenticationBackend"
    
    if experimental_backend not in backends:
        backends.insert(0, experimental_backend)
        
    settings["AUTHENTICATION_BACKENDS"] = backends