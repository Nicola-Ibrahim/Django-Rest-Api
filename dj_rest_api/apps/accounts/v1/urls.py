from django.urls import path

from .views import ProfileDetailsUpdateView, UserDetailsUpdateDestroyView, UserListCreateView, VerifyUserAccount

app_name = "accounts-v1"

urlpatterns = [
    path("", UserListCreateView.as_view(), name="list-create-users"),
    path("<uuid:id>/", UserDetailsUpdateDestroyView.as_view(), name="user-details-update-destroy"),
    path("<uuid:id>/profile/", ProfileDetailsUpdateView.as_view(), name="profile-details-update"),
    path("verify/", VerifyUserAccount.as_view(), name="verify-account"),
]
