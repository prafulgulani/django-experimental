from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.experimental.flags import is_experiment_enabled


def superuser_required(
    view_func=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url="admin:login",
):
    """
    Decorator for views that checks that the user is logged in and is a
    superuser, raising PermissionDenied or redirecting to the login page.
    """
    if not is_experiment_enabled("ENABLE_SUPERUSER_REQUIRED"):
        raise ImproperlyConfigured(
            "superuser_required cannot be used because the experimental flag "
            "'ENABLE_SUPERUSER_REQUIRED' is not enabled in settings.py."
        )

    def check_superuser(user):
        if not (user.is_authenticated and user.is_active):
            return False
        if user.is_superuser:
            return True
        raise PermissionDenied

    actual_decorator = user_passes_test(
        check_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if view_func:
        return actual_decorator(view_func)
    return actual_decorator