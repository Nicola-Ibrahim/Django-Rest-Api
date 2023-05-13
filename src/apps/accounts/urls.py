from django.urls import path

from .api.views import (
    UserDeleteView,
    UserDetailsView,
    UserLoginView,
    UserSignView,
    UsersListView,
    UserUpdateView,
    VerifyEmail,
)

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("verify_email/", VerifyEmail.as_view(), name="email-verify"),
    path("list/<str:user_type>/", UsersListView.as_view(), name="list"),
    path("details/", UserDetailsView.as_view(), name="details"),
    path("delete/", UserDeleteView.as_view(), name="delete"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("signup/<str:user_type>/", UserSignView.as_view(), name="signup"),
]
