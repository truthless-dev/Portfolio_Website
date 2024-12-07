from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="braille"),
    path("back-translate", views.back_translate, name="back_translate"),
]
