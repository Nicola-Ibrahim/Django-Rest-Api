from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "auth"

urlpatterns = [
    path("", views.UserListView.as_view(), name="list-users"),
    path("<str:user_type>/", views.UserCreateView.as_view(), name="create-user"),
    path("<slug>", views.UserDetailsUpdateDestroyView.as_view(), name="details"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify_email/", views.VerifyAccount.as_view(), name="email-verify"),
]
