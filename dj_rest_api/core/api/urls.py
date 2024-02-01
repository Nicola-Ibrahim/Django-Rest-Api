from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("v1/accounts/", include("apps.accounts.v1.urls", namespace="accounts-api-v1")),
    path("v1/auth/", include("apps.authentication.v1.urls", namespace="auth-api-v1")),
]
