from apps.api.base.views import LanguagesListView
from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("languages/", LanguagesListView.as_view(), name="languages-lits"),
    path("api/accounts/", include("apps.api.accounts.urls", namespace="accounts-api")),
    path("api/auth/", include("apps.api.authentication.urls", namespace="auth-api")),
]
