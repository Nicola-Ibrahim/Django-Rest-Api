from django.urls import include, path

urlpatterns = [
    path("v1/accounts/", include("apps.accounts.v1.urls", namespace="accounts-v1")),
    path("v1/auth/", include("apps.authentication.v1.urls", namespace="auth-v1")),
]
