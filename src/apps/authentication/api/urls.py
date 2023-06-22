from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ChangePasswordView,
    FirstTimePasswordView,
    ForgetPasswordRequestView,
    ForgetPasswordView,
    LoginView,
    LogoutView,
    VerifyOTPNumberView,
)

app_name = "auth"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("login/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "forget_password_request/",
        ForgetPasswordRequestView.as_view(),
        name="forget-password-request",
    ),
    path("otp/verify/", VerifyOTPNumberView.as_view(), name="verify-top"),
    path("forget_password/", ForgetPasswordView.as_view(), name="forget-password"),
    path("change_password/", ChangePasswordView.as_view(), name="change-password"),
    path(
        "first_time_password/",
        FirstTimePasswordView.as_view(),
        name="First-Time-password",
    ),
]
