from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    usable_password = None
    captcha = ReCaptchaField()

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "captcha",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email is None:
            return email
        user_model = self._meta.model
        if user_model.objects.filter(email__iexact=email).exists():
            self.add_error("email", "A user with that email already exists.")
        return email
