from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path("", views.UserListView.as_view(), name="list-users"),
    path("<str:user_type>/create/", views.UserCreateView.as_view(), name="create-user"),
    path(
        "<uuid:id>/",
        views.UserDetailsUpdateDestroyView.as_view(),
        name="user-details-update-destroy",
    ),
    # path("<uuid:id>/profile", views.ProfileDetailsUpdateDestroyView.as_view(), name="profile-update-destroy-user"),
    path("verify_email/", views.VerifyAccount.as_view(), name="email-verify"),
    path(
        "forget_password_request/",
        views.ForgetPasswordRequestView.as_view(),
        name="forget-password-request",
    ),
    path(
        "forget_password/", views.ForgetPasswordView.as_view(), name="forget-password"
    ),
    path(
        "change_password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path(
        "first_time_password/",
        views.FirstTimePasswordView.as_view(),
        name="first-time-password",
    ),
    path("otp/verify/", views.VerifyOTPNumberView.as_view(), name="verify-top"),
]
