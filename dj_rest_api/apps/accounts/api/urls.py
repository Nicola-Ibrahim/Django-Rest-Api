from django.urls import path

from .views import (
    ChangePasswordView,
    FirstTimePasswordView,
    ForgetPasswordRequestView,
    ForgetPasswordView,
    UserDetailsUpdateDestroyView,
    UserListCreateView,
    VerifyOTPNumberView,
    VerifyUserAccount,
)

app_name = "accounts"

urlpatterns = [
    path("", UserListCreateView.as_view(), name="list-users"),
    path(
        "<uuid:id>/",
        UserDetailsUpdateDestroyView.as_view(),
        name="user-details-update-destroy",
    ),
    # path("<uuid:id>/profile", ProfileDetailsUpdateDestroyView.as_view(), name="profile-update-destroy-user"),
    path("verify_email/", VerifyUserAccount.as_view(), name="email-verify"),
    path(
        "forget_password_request/",
        ForgetPasswordRequestView.as_view(),
        name="forget-password-request",
    ),
    path("forget_password/", ForgetPasswordView.as_view(), name="forget-password"),
    path("change_password/", ChangePasswordView.as_view(), name="change-password"),
    path(
        "first_time_password/",
        FirstTimePasswordView.as_view(),
        name="first-time-password",
    ),
    path("otp/verify/", VerifyOTPNumberView.as_view(), name="verify-top"),
]
