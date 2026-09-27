from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path(
        "admin/secure-superuser-view/",
        views.superuser_secure_view,
        name="superuser_secure_view",
    ),
    path(
        "admin/secure-superuser-view2/",
        views.superuser_secure_view_custom_field,
        name="superuser_secure_view_custom_field",
    ),
    path("admin/", admin.site.urls),
]