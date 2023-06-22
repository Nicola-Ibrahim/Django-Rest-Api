from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserDeleteView,
    UserDetailsView,
    UserSignView,
    UsersListView,
    UserUpdateView,
    VerifyAccount,
)

app_name = "auth"

urlpatterns = [
    path("verify_email/", VerifyAccount.as_view(), name="email-verify"),
    path("users/", UsersListView.as_view(), name="list"),
    path("users/<slug>", UserDetailsView.as_view(), name="details"),
    path("delete/", UserDeleteView.as_view(), name="delete"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("signup/<str:user_type>/", UserSignView.as_view(), name="signup"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
