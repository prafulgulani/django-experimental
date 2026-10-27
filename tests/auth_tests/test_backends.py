from django.contrib.auth import authenticate, get_user_model
from django.test import RequestFactory, TestCase, override_settings

from django.experimental.contrib.auth.backends import DualAuthenticationBackend

User = get_user_model()


class DualAuthenticationBackendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="johndoe",
            email="johndoe@example.com",
            password="correctpassword123",
            name="John Doe",
        )
        cls.inactive_user = User.objects.create_user(
            username="inactiveuser",
            email="inactive@example.com",
            password="correctpassword123",
            name="Inactive User",
            is_active=False,
        )
        cls.factory = RequestFactory()
        cls.backend = DualAuthenticationBackend()

    def test_authenticate_with_exact_username(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username="johndoe", password="correctpassword123"
        )
        self.assertEqual(user, self.user)

    def test_authenticate_with_case_insensitive_username(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username="JohnDoe", password="correctpassword123"
        )
        self.assertEqual(user, self.user)

    def test_authenticate_with_exact_email(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username="johndoe@example.com", password="correctpassword123"
        )
        self.assertEqual(user, self.user)

    def test_authenticate_with_case_insensitive_email(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username="JohnDoe@EXAMPLE.COM", password="correctpassword123"
        )
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_password_returns_none(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username="johndoe", password="wrongpassword"
        )
        self.assertIsNone(user)

    def test_authenticate_with_nonexistent_user_returns_none(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username="ghostuser", password="anypassword"
        )
        self.assertIsNone(user)

    def test_authenticate_inactive_user_returns_none(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username="inactiveuser", password="correctpassword123"
        )
        self.assertIsNone(user)

    def test_authenticate_with_none_username_returns_none(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username=None, password="correctpassword123"
        )
        self.assertIsNone(user)

    def test_authenticate_with_none_password_returns_none(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username="johndoe", password=None
        )
        self.assertIsNone(user)

    def test_authenticate_via_kwargs_username_field(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request,
            password="correctpassword123",
            **{User.USERNAME_FIELD: "johndoe"},
        )
        self.assertEqual(user, self.user)

    @override_settings(DJANGO_EXPERIMENTAL_FLAGS={"ENABLE_NEWAUTH": False})
    def test_authenticate_returns_none_when_feature_flag_is_disabled(self):
        request = self.factory.get("/")
        user = self.backend.authenticate(
            request, username="johndoe", password="correctpassword123"
        )
        self.assertIsNone(user)

    def test_django_authenticate_helper_integration(self):
        request = self.factory.get("/")
        user_by_username = authenticate(
            request, username="johndoe", password="correctpassword123"
        )
        user_by_email = authenticate(
            request, username="johndoe@example.com", password="correctpassword123"
        )
        self.assertEqual(user_by_username, self.user)
        self.assertEqual(user_by_email, self.user)