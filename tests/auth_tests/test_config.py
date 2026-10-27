from django.test import SimpleTestCase

from django.experimental.contrib.auth.config import modify_settings


class ModifySettingsTests(SimpleTestCase):
    def test_default_auth_user_model_swapped_to_experimental_user(self):
        settings_dict = {"AUTH_USER_MODEL": "auth.User"}
        modify_settings(settings_dict)
        self.assertEqual(
            settings_dict["AUTH_USER_MODEL"], "experimental_auth.User"
        )

    def test_missing_auth_user_model_defaults_to_experimental_user(self):
        settings_dict = {}
        modify_settings(settings_dict)
        self.assertEqual(
            settings_dict["AUTH_USER_MODEL"], "experimental_auth.User"
        )

    def test_custom_user_model_is_preserved(self):
        settings_dict = {"AUTH_USER_MODEL": "custom_app.CustomUser"}
        modify_settings(settings_dict)
        self.assertEqual(
            settings_dict["AUTH_USER_MODEL"], "custom_app.CustomUser"
        )

    def test_experimental_backend_prepended_to_default_backends(self):
        settings_dict = {}
        modify_settings(settings_dict)
        expected_backends = [
            "django.experimental.contrib.auth.backends.DualAuthenticationBackend",
            "django.contrib.auth.backends.ModelBackend",
        ]
        self.assertEqual(
            settings_dict["AUTHENTICATION_BACKENDS"], expected_backends
        )

    def test_experimental_backend_prepended_to_existing_custom_backends(self):
        settings_dict = {
            "AUTHENTICATION_BACKENDS": [
                "my_custom_app.backends.TokenBackend",
                "django.contrib.auth.backends.ModelBackend",
            ]
        }
        modify_settings(settings_dict)
        self.assertEqual(
            settings_dict["AUTHENTICATION_BACKENDS"][0],
            "django.experimental.contrib.auth.backends.DualAuthenticationBackend",
        )
        self.assertIn(
            "my_custom_app.backends.TokenBackend",
            settings_dict["AUTHENTICATION_BACKENDS"],
        )
        self.assertEqual(len(settings_dict["AUTHENTICATION_BACKENDS"]), 3)

    def test_experimental_backend_not_duplicated_if_already_present(self):
        backend_path = (
            "django.experimental.contrib.auth.backends.DualAuthenticationBackend"
        )
        settings_dict = {
            "AUTHENTICATION_BACKENDS": [
                backend_path,
                "django.contrib.auth.backends.ModelBackend",
            ]
        }
        modify_settings(settings_dict)
        self.assertEqual(
            settings_dict["AUTHENTICATION_BACKENDS"].count(backend_path), 1
        )

    def test_tuple_backends_converted_to_list_cleanly(self):
        settings_dict = {
            "AUTHENTICATION_BACKENDS": (
                "django.contrib.auth.backends.ModelBackend",
            )
        }
        modify_settings(settings_dict)
        self.assertIsInstance(settings_dict["AUTHENTICATION_BACKENDS"], list)
        self.assertEqual(
            settings_dict["AUTHENTICATION_BACKENDS"][0],
            "django.experimental.contrib.auth.backends.DualAuthenticationBackend",
        )