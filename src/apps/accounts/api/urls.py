from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserDeleteView,
    UserDetailsView,
    UsersListCreateView,
    UserUpdateView,
    VerifyAccount,
)

app_name = "auth"

urlpatterns = [
    path("", UsersListCreateView.as_view(), name="list-create-user"),
    path("users/<slug>", UserDetailsView.as_view(), name="details"),
    path("delete/", UserDeleteView.as_view(), name="delete"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify_email/", VerifyAccount.as_view(), name="email-verify"),
]
