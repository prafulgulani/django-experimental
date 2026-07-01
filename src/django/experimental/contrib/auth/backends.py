from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.experimental.flags import is_experiment_enabled


class DualAuthenticationBackend(ModelBackend):
    """
    Custom authentication backend allowing users to log in using 
    either username or email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not is_experiment_enabled("ENABLE_NEWAUTH"):
            return None
        
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return None

        try:
            user = UserModel._default_manager.get(
                Q(**{UserModel.USERNAME_FIELD + "__iexact": username}) |
                Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None