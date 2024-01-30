from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("accounts/", include("apps.accounts.urls")),
    path("auth/", include("apps.authentication.urls")),
]
