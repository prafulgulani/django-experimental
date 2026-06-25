from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NewUser


class NewUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = NewUser
        fields = ("username", "email", "name")


class NewUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = NewUser
        fields = ("username", "email", "name", "is_active", "is_staff")