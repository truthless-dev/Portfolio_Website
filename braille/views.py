from django.shortcuts import render


def index(request):
    context = {
        "title": "Braille",
    }
    return render(request, "braille/index.html", context)
