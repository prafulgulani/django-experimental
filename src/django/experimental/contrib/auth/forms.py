import unicodedata
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm, 
    UserChangeForm as DjangoUserChangeForm
)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import AbstractUser


class UsernameField(forms.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        if self.max_length is not None and len(value) > self.max_length:
            return value
        return unicodedata.normalize("NFKC", value)

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
        }


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = AbstractUser
        fields = ("username", "email", "name")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        UserModel = get_user_model()
        self._meta.model = UserModel
        self.fields["username"].model = UserModel

    def clean_username(self):
        username = self.cleaned_data.get("username")
        UserModel = get_user_model()
        if (
            username
            and UserModel._default_manager.filter(username__iexact=username).exists()
        ):
            raise ValidationError(
                _("A user with that username already exists."),
                code="unique",
            )
        return username


class UserChangeForm(DjangoUserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see "
            "the user’s password."
        ),
    )

    class Meta(DjangoUserChangeForm.Meta):
        model = AbstractUser
        fields = ("username", "email", "name", "is_active", "is_staff")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        UserModel = get_user_model()
        self._meta.model = UserModel
        self.fields["username"].model = UserModel