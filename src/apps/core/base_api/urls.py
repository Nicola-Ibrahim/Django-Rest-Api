from django.urls import path

from .views import LanguagesListView

urlpatterns = [
    path("languages/", LanguagesListView.as_view(), name="languages-lits"),
]
