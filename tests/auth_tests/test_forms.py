from django.contrib.auth import get_user_model
from django.test import TestCase

from django.experimental.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    UsernameField,
)

User = get_user_model()


class UsernameFieldTests(TestCase):
    def test_widget_attributes_include_autocapitalize_and_autocomplete(self):
        field = UsernameField()
        attrs = field.widget_attrs(field.widget)
        self.assertEqual(attrs.get("autocapitalize"), "none")
        self.assertEqual(attrs.get("autocomplete"), "username")

    def test_to_python_normalizes_nfkc_unicode(self):
        field = UsernameField()
        # Non-normalized fullwidth characters
        fullwidth_str = "\uff46\uff55\uff4c\uff4c\uff57\uff49\uff44\uff54\uff48"
        normalized_str = "fullwidth"
        self.assertEqual(field.to_python(fullwidth_str), normalized_str)


class UserCreationFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.existing_user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="password123",
            name="Existing User",
        )

    def test_valid_user_creation_saves_successfully(self):
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "name": "New User",
            "password1": "complexpassword123!",
            "password2": "complexpassword123!",
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertEqual(user.name, "New User")
        self.assertTrue(user.check_password("complexpassword123!"))

    def test_clean_username_rejects_case_insensitive_duplicate(self):
        form_data = {
            "username": "ExistingUser",
            "email": "another@example.com",
            "name": "Test Name",
            "password1": "complexpassword123!",
            "password2": "complexpassword123!",
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertEqual(
            form.errors["username"],
            ["A user with that username already exists."],
        )


class UserChangeFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="sampleuser",
            email="sample@example.com",
            password="password123",
            name="Sample Name",
        )

    def test_form_initializes_with_correct_fields_and_metadata(self):
        form = UserChangeForm(instance=self.user)
        self.assertIn("username", form.fields)
        self.assertIn("email", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("password", form.fields)
        self.assertEqual(form.instance.pk, self.user.pk)

    def test_form_updates_user_attributes(self):
        form_data = {
            "username": "updatedusername",
            "email": "updated@example.com",
            "name": "Updated Name",
            "is_active": True,
            "is_staff": False,
        }
        form = UserChangeForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        updated_user = form.save()
        self.assertEqual(updated_user.name, "Updated Name")
        self.assertEqual(updated_user.email, "updated@example.com")