from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordView,
    FirstTimePasswordView,
    ForgetPasswordRequestView,
    ForgetPasswordView,
    LoginView,
    LogoutView,
    UserDeleteView,
    UserDetailsView,
    UserSignView,
    UsersListView,
    UserUpdateView,
    VerifyAccount,
    VerifyOTPNumberView,
)

app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("login/", LogoutView.as_view(), name="logout"),
    path("verify_email/", VerifyAccount.as_view(), name="email-verify"),
    path("users/", UsersListView.as_view(), name="list"),
    path("users/<slug>", UserDetailsView.as_view(), name="details"),
    path("delete/", UserDeleteView.as_view(), name="delete"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("signup/<str:user_type>/", UserSignView.as_view(), name="signup"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("forget_password_request/", ForgetPasswordRequestView.as_view(), name="forget-password-request"),
    path("otp/verify/", VerifyOTPNumberView.as_view(), name="verify-top"),
    path("forget_password/", ForgetPasswordView.as_view(), name="forget-password"),
    path("change_password/", ChangePasswordView.as_view(), name="change-password"),
    path("first_time_password/", FirstTimePasswordView.as_view(), name="First-Time-password"),
]
