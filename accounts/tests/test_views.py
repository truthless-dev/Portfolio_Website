from http import HTTPStatus
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django_recaptcha.client import RecaptchaResponse


class TestProfileView(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("profile")
        user_model = get_user_model()
        cls.user1 = user_model.objects.create_user(
            username="User1",
            email="user1@test.com",
            password="User1Password",
        )

    def test_redirect_anonymous_user_to_login(self):
        login_url = reverse("login")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, login_url)

    def test_show_authenticated_user_their_profile(self):
        username = self.user1.get_username()
        profile_url = reverse("user_profile", kwargs={"username": username})
        self.client.force_login(self.user1)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, profile_url)


class TestUserProfileView(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("profile")
        user_model = get_user_model()
        cls.user1 = user_model.objects.create_user(
            username="User1",
            email="user1@test.com",
            password="User1Password",
        )

    def _get_profile(self, username: str):
        url = reverse("user_profile", kwargs={"username": username})
        response = self.client.get(url, follow=True)
        return response

    def test_raise_not_found_error_for_nonexistent_username(self):
        response = self._get_profile("NonexistentUser")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_profile_owner_can_view_private_data(self):
        self.client.force_login(self.user1)
        response = self._get_profile(self.user1.get_username())
        is_my_profile = response.context.get("is_my_profile")
        self.assertTrue(is_my_profile)

    def test_third_party_cannot_view_private_data(self):
        response = self._get_profile(self.user1.get_username())
        is_my_profile = response.context.get("is_my_profile")
        self.assertFalse(is_my_profile)


class TestRegistrationView(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("register")

    @patch("django_recaptcha.fields.client.submit")
    def _test_registration_view_with_mock_recaptcha(
        self,
        mock_recaptcha,
        form_data: dict,
    ):
        mock_recaptcha.return_value = RecaptchaResponse(is_valid=True)
        form_data = form_data.copy()
        if "g-recaptcha-response" not in form_data:
            form_data["g-recaptcha-response"] = "PASSED"
        response = self.client.post(self.url, data=form_data, follow=True)
        return response

    def test_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_display_form_again_for_invalid_input(self):
        # Invalidate form by providing non-matching passwords.
        form_data = {
            "username": "NewTestUser",
            "email": "newtestuser@test.com",
            "password1": "PasswordsDo",
            "password2": "NotMatch",
        }
        response = self._test_registration_view_with_mock_recaptcha(
            form_data=form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        form = response.context["form"]
        form_errors = form.errors.as_data()
        error_count = len(form_errors)
        self.assertEqual(error_count, 1)
        password_errors = form_errors.get("password2")
        self.assertIsNotNone(password_errors)

    def test_redirect_to_new_profile_for_valid_input(self):
        username = "NewTestUser"
        form_data = {
            "username": username,
            "email": "newtestuser@test.com",
            "password1": "SecureTestPasswordForNewUser",
            "password2": "SecureTestPasswordForNewUser",
        }
        destination_url = reverse("user_profile", kwargs={"username": username})
        response = self._test_registration_view_with_mock_recaptcha(
            form_data=form_data,
        )
        self.assertRedirects(response, destination_url)
