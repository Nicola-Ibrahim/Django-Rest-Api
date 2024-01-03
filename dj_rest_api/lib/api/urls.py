from django.urls import include, path

from .views import LanguagesListView

app_name = "api"

urlpatterns = [
    path("languages/", LanguagesListView.as_view(), name="languages-lits"),
    path("accounts/", include("apps.accounts.api.urls", namespace="accounts-api")),
    path("auth/", include("apps.authentication.api.urls", namespace="auth-api")),
]
