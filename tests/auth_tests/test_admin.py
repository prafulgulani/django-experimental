from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase

from django.experimental.contrib.auth.admin import UserAdmin
from django.experimental.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class MockRequest:
    pass


class UserAdminTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.site = AdminSite()
        cls.user_admin = UserAdmin(User, cls.site)

    def test_user_model_is_registered_with_user_admin(self):
        self.assertIn(User, admin.site._registry)
        self.assertIsInstance(admin.site._registry[User], UserAdmin)

    def test_custom_forms_assigned_to_admin(self):
        self.assertIs(self.user_admin.form, UserChangeForm)
        self.assertIs(self.user_admin.add_form, UserCreationForm)

    def test_list_display_includes_name_and_omits_split_name_fields(self):
        expected_list_display = ("username", "email", "name", "is_staff", "is_active")
        self.assertEqual(self.user_admin.list_display, expected_list_display)
        self.assertNotIn("first_name", self.user_admin.list_display)
        self.assertNotIn("last_name", self.user_admin.list_display)

    def test_search_fields_includes_name(self):
        self.assertEqual(
            self.user_admin.search_fields,
            ("username", "email", "name"),
        )
        self.assertNotIn("first_name", self.user_admin.search_fields)
        self.assertNotIn("last_name", self.user_admin.search_fields)

    def test_list_filter_configuration(self):
        expected_list_filter = ("is_staff", "is_superuser", "is_active", "groups")
        self.assertEqual(self.user_admin.list_filter, expected_list_filter)

    def test_fieldsets_contain_name_and_exclude_first_and_last_name(self):
        all_fieldset_fields = [
            field
            for _, fieldset_options in self.user_admin.fieldsets
            for field in fieldset_options.get("fields", ())
        ]
        self.assertIn("name", all_fieldset_fields)
        self.assertIn("email", all_fieldset_fields)
        self.assertNotIn("first_name", all_fieldset_fields)
        self.assertNotIn("last_name", all_fieldset_fields)

    def test_add_fieldsets_contain_name_and_passwords(self):
        all_add_fieldset_fields = [
            field
            for _, fieldset_options in self.user_admin.add_fieldsets
            for field in fieldset_options.get("fields", ())
        ]
        self.assertIn("name", all_add_fieldset_fields)
        self.assertIn("username", all_add_fieldset_fields)
        self.assertIn("email", all_add_fieldset_fields)
        self.assertIn("password1", all_add_fieldset_fields)
        self.assertIn("password2", all_add_fieldset_fields)
        self.assertNotIn("first_name", all_add_fieldset_fields)
        self.assertNotIn("last_name", all_add_fieldset_fields)