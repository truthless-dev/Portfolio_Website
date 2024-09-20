from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            extra_context={
                "title": "Login",
            },
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change_form.html",
            extra_context={
                "title": "Change Password",
            },
        ),
        name="password_change",
    ),
    path(
        "password_change_done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html",
            extra_context={
                "title": "Password Changed",
            },
        ),
        name="password_change_done",
    ),
]
