from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import User
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(DjangoUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    
    list_display = ("username", "email", "name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email", "name")
    ordering = ("username",)
    
    filter_horizontal = ("groups", "user_permissions")

    readonly_fields = ("date_joined", "last_login")
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal Info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important Dates"), {"fields": ("date_joined", "last_login")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("name", "username", "email", "password1", "password2"),
        }),
    )


# Only register the base admin if the user hasn't swapped the model for a custom subclass
if settings.AUTH_USER_MODEL == "experimental_auth.User":
    admin.site.register(User, UserAdmin)