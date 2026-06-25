from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser
from .forms import NewUserCreationForm, NewUserChangeForm


@admin.register(NewUser)
class NewUserAdmin(UserAdmin):
    add_form = NewUserCreationForm
    form = NewUserChangeForm
    
    list_display = ("name", "username", "email", "is_staff", "is_active")
    search_fields = ("name", "username", "email")
    
    readonly_fields = ("date_joined", "last_login")
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("date_joined", "last_login")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("name", "username", "email", "password1", "password2"),
        }),
    )