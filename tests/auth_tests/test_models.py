from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user_normalizes_email(self):
        user = User.objects.create_user(
            username="johndoe",
            email="JohnDoe@EXAMPLE.COM",
            password="securepassword123",
        )
        # Django's normalize_email only lowercases the domain portion
        self.assertEqual(user.email, "JohnDoe@example.com")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_without_username_raises_value_error(self):
        with self.assertRaisesMessage(ValueError, "The Username field must be set"):
            User.objects.create_user(
                username="",
                email="user@example.com",
                password="securepassword123",
            )

    def test_create_user_without_email_raises_value_error(self):
        with self.assertRaisesMessage(ValueError, "The Email field must be set"):
            User.objects.create_user(
                username="johndoe",
                email="",
                password="securepassword123",
            )

    def test_create_superuser_sets_staff_and_superuser(self):
        admin = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword123",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_create_superuser_is_staff_false_raises_value_error(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(
                username="adminuser",
                email="admin@example.com",
                password="adminpassword123",
                is_staff=False,
            )

    def test_create_superuser_is_superuser_false_raises_value_error(self):
        with self.assertRaisesMessage(
            ValueError, "Superuser must have is_superuser=True."
        ):
            User.objects.create_superuser(
                username="adminuser",
                email="admin@example.com",
                password="adminpassword123",
                is_superuser=False,
            )


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="password123",
            name="Alice Smith",
        )

    def test_get_full_name_returns_name(self):
        self.assertEqual(self.user.get_full_name(), "Alice Smith")

    def test_get_short_name_returns_first_word_of_name(self):
        self.assertEqual(self.user.get_short_name(), "Alice")

    def test_get_short_name_falls_back_to_username_when_name_blank(self):
        user_no_name = User.objects.create_user(
            username="bob",
            email="bob@example.com",
            password="password123",
            name="",
        )
        self.assertEqual(user_no_name.get_short_name(), "bob")

    def test_unique_email_constraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    username="alice2",
                    email="alice@example.com",
                    password="password123",
                )

    def test_unique_username_constraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    username="alice",
                    email="alice2@example.com",
                    password="password123",
                )