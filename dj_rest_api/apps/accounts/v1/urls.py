from django.urls import path

from .views import ProfileDetailsUpdateView, UserDetailsUpdateDestroyView, UserListCreateView, VerifyUserAccount

app_name = "accounts-api-v1"

urlpatterns = [
    path("", UserListCreateView.as_view(), name="list-create-users"),
    path("<uuid:id>", UserDetailsUpdateDestroyView.as_view(), name="user-details-update-destroy"),
    path("<uuid:id>/profile", ProfileDetailsUpdateView.as_view(), name="profile-details-update"),
    path("verify_email", VerifyUserAccount.as_view(), name="email-verify"),
]
