from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django_recaptcha.client import RecaptchaResponse

from accounts.forms import UserRegistrationForm


class TestUserCreation(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_model = get_user_model()
        cls.user1 = user_model.objects.create_user(
            username="User1",
            email="user1@test.com",
            password="User1Password",
        )

    @patch("django_recaptcha.fields.client.submit")
    def _test_form_with_mock_recaptcha(
        self,
        mock_recaptcha,
        form_data: dict,
        field: str | None = None,
        error_message: list[str] | str | None = None,
    ):
        mock_recaptcha.return_value = RecaptchaResponse(is_valid=True)
        form_data = form_data.copy()
        if "g-recaptcha-response" not in form_data:
            form_data["g-recaptcha-response"] = "PASSED"
        form = UserRegistrationForm(form_data)
        if field is not None and error_message is not None:
            self.assertFormError(form, field, error_message)
        else:
            self.assertTrue(form.is_valid())
            form.save()

    def test_username_already_exists(self):
        form_data = {
            "username": "User1",
            "email": "user1@email.com",
            "password1": "User1Password",
            "password2": "User1Password",
        }
        self._test_form_with_mock_recaptcha(
            form_data=form_data,
            field="username",
            error_message="A user with that username already exists.",
        )

    def test_username_already_exists_with_different_case(self):
        form_data = {
            "username": "uSeR1",
            "email": "user1@email.com",
            "password1": "User1Password",
            "password2": "User1Password",
        }
        self._test_form_with_mock_recaptcha(
            form_data=form_data,
            field="username",
            error_message="A user with that username already exists.",
        )

    def test_email_already_exists(self):
        form_data = {
            "username": "User2",
            "email": "user1@test.com",
            "password1": "User1Password",
            "password2": "User1Password",
        }
        self._test_form_with_mock_recaptcha(
            form_data=form_data,
            field="email",
            error_message="A user with that email already exists.",
        )

    def test_email_already_exists_with_different_case(self):
        form_data = {
            "username": "User2",
            "email": "uSeR1@Test.Com",
            "password1": "User1Password",
            "password2": "User1Password",
        }
        self._test_form_with_mock_recaptcha(
            form_data=form_data,
            field="email",
            error_message="A user with that email already exists.",
        )

    def test_new_user_is_created(self):
        form_data = {
            "username": "User2",
            "email": "user2@test.com",
            "password1": "User2Password",
            "password2": "User2Password",
        }
        self._test_form_with_mock_recaptcha(form_data=form_data)
        created = get_user_model().objects.filter(username__exact="User2").exists()
        self.assertTrue(created)
