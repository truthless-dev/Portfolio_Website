from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.http import Http404


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        args = {f"{self.model.USERNAME_FIELD}__iexact": username}
        return self.get(**args)

    def get_by_natural_key_or_404(self, username):
        try:
            return self.get_by_natural_key(username)
        except self.model.DoesNotExist:
            raise Http404(f"No {self.model._meta.object_name} matches the given query.")


class User(AbstractUser):
    """
    Custom User model

    This model stores the user's username as it was entered upon
    creation, but overrides `.get_by_natural_key` to search for user-
    names case-insensitively. It also adds a case-insensitive unique
    constraint upon its associated `username` column.
    """

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("username"),
                name="%(app_label)s_%(class)s_username_unique_case_insensitive",
            ),
            models.UniqueConstraint(
                models.functions.Lower("email"),
                name="%(app_label)s_%(class)s_email_unique_case_insensitive",
            ),
        ]
