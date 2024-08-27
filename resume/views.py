from django.shortcuts import render


def index(request):
    context = {
        "title": "Resume",
    }
    return render(request, "resume/index.html", context)
