from unittest.mock import patch
from django.conf import settings
from django.core import checks
from django.db import models
from django.test import SimpleTestCase, override_settings

from django.experimental.contrib.auth.apps import check_experimental_user_subclass
from django.experimental.contrib.auth.models import AbstractUser, User


class ExperimentalAuthChecksTests(SimpleTestCase):
    def test_check_passes_with_default_experimental_user(self):
        errors = check_experimental_user_subclass(None)
        self.assertEqual(errors, [])

    @override_settings(AUTH_USER_MODEL="invalid_model_format")
    def test_check_e001_invalid_model_string_format(self):
        errors = check_experimental_user_subclass(None)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].id, "experimental_auth.E001")
        self.assertIn("invalid_model_format", errors[0].msg)

    @override_settings(AUTH_USER_MODEL="nonexistent_app.UserModel")
    def test_check_e001_lookup_error_for_missing_app(self):
        errors = check_experimental_user_subclass(None)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].id, "experimental_auth.E001")

    @override_settings(AUTH_USER_MODEL="some_app.NonSubclassUser")
    def test_check_e002_model_not_subclassing_abstract_user(self):
        class NonSubclassUser(models.Model):
            class Meta:
                app_label = "some_app"

        with patch("django.apps.apps.get_model", return_value=NonSubclassUser):
            errors = check_experimental_user_subclass(None)
            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0].id, "experimental_auth.E002")
            self.assertIn("ENABLE_NEWAUTH", errors[0].msg)
            self.assertIn("some_app.NonSubclassUser", errors[0].msg)

    @override_settings(AUTH_USER_MODEL="some_app.ValidCustomUser")
    def test_check_passes_with_custom_subclass_of_abstract_user(self):
        class ValidCustomUser(AbstractUser):
            class Meta:
                app_label = "some_app"

        with patch("django.apps.apps.get_model", return_value=ValidCustomUser):
            errors = check_experimental_user_subclass(None)
            self.assertEqual(errors, [])