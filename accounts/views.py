from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render

from .forms import UserRegistrationForm


def profile(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        return redirect("user_profile", username=username)
    return redirect("login")


def user_profile(request, username):
    model = get_user_model()
    profile_user = model.objects.get_by_natural_key_or_404(username)
    is_my_profile = request.user.pk == profile_user.pk
    context = {
        "title": f"{username}'s Profile",
        "profile_user": profile_user,
        "is_my_profile": is_my_profile,
    }
    return render(request, "accounts/user_profile.html", context)


def register(request):
    title = "New User Registration"
    if request.method != "POST":
        # First visit. Simply display the page.
        form = UserRegistrationForm()
        context = {
            "title": title,
            "form": form,
        }
        return render(request, "accounts/register.html", context)

    form = UserRegistrationForm(request.POST)
    if not form.is_valid():
        context = {
            "title": title,
            "form": form,
        }
        return render(request, "accounts/register.html", context)

    # Validation passed. Log the new user in.
    form.save()
    username = form.cleaned_data["username"]
    password = form.cleaned_data["password1"]
    new_user = authenticate(request, username=username, password=password)
    if new_user is not None:
        login(request, new_user)
        return redirect("user_profile", username=new_user.username)
    return redirect("login")
