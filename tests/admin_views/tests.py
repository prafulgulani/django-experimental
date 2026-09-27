from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.test import TestCase, override_settings
from django.urls import reverse

from django.experimental.contrib.admin.views.decorators import superuser_required

User = get_user_model()


@override_settings(
    ROOT_URLCONF="admin_views.urls",
    DJANGO_EXPERIMENTAL_FLAGS={"ENABLE_SUPERUSER_REQUIRED": True},
)
class SuperuserSecureViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username="super", password="password", email="super@example.com"
        )
        cls.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        cls.regular_user = User.objects.create_user(
            username="regular", password="password", is_staff=False
        )

    def test_secure_view_shows_login_if_not_logged_in(self):
        secure_url = reverse("superuser_secure_view")
        response = self.client.get(secure_url)
        self.assertRedirects(
            response, "%s?next=%s" % (reverse("admin:login"), secure_url)
        )
        response = self.client.get(secure_url, follow=True)
        self.assertTemplateUsed(response, "admin/login.html")
        self.assertEqual(response.context[REDIRECT_FIELD_NAME], secure_url)

    def test_superuser_required_decorator_works_with_custom_redirect_field(self):
        secure_url = reverse("superuser_secure_view_custom_field")
        response = self.client.get(secure_url)
        self.assertRedirects(
            response, "%s?myfield=%s" % (reverse("admin:login"), secure_url)
        )

    def test_authenticated_staff_denied_403(self):
        self.client.login(username="staff", password="password")
        secure_url = reverse("superuser_secure_view")
        response = self.client.get(secure_url)
        self.assertEqual(response.status_code, 403)

    def test_authenticated_regular_user_denied_403(self):
        self.client.login(username="regular", password="password")
        secure_url = reverse("superuser_secure_view")
        response = self.client.get(secure_url)
        self.assertEqual(response.status_code, 403)

    def test_superuser_access_allowed(self):
        self.client.login(username="super", password="password")
        secure_url = reverse("superuser_secure_view")
        response = self.client.get(secure_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Superuser Secure View")

    @override_settings(DJANGO_EXPERIMENTAL_FLAGS={"ENABLE_SUPERUSER_REQUIRED": False})
    def test_disabled_flag_raises_improperly_configured(self):
        def dummy_view(request):
            return HttpResponse("OK")

        with self.assertRaises(ImproperlyConfigured):
            superuser_required(dummy_view)