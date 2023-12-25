from django.urls import path

from .views import UserDetailsUpdateDestroyView, UserListCreateView, VerifyUserAccount

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
]
