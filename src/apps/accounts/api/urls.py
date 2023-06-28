from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "auth"

urlpatterns = [
    path("", views.UserListCreateView.as_view(), name="list-create-users"),
    path("<uuid:id>/", views.UserDetailsUpdateDestroyView.as_view(), name="details-update-destroy-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify_email/", views.VerifyAccount.as_view(), name="email-verify"),
]
