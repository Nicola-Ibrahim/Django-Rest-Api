from django.urls import reverse
from hypothesis import HealthCheck, Verbosity, example, given, settings
from hypothesis import strategies as st
from hypothesis.extra.django import from_model
from rest_framework.test import force_authenticate

from ...accounts import views
from ...models import User


class TestAccountsViews:
    # Define a strategy for generating users
    user_strategy: st.SearchStrategy = from_model(User)

    # Edit suppress_health_check for using `mocker` fixture
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=100,
    )
    @given(users=st.lists(user_strategy, min_size=1, max_size=4))
    def test_length_of_created_users(self, users, mocker, rf):
        # Arrange
        url = reverse("accounts-api:list-users")
        request = rf.get(url)

        view = views.UserListCreateView.as_view()

        # Mock the queryset function in the view
        mocker.patch.multiple(
            views.UserListView,
            check_permissions=mocker.MagicMock(return_value=True),
            get_queryset=mocker.MagicMock(return_value=users),
        )
        # Act
        response = view(request).render()

        # Assert
        assert response.status_code == 200
        assert len(response.data["data"]) == len(users)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
    )
    @given(user=user_strategy)
    def test_retrieve_user_view(self, user, mocker, rf):
        # Arrange
        url = reverse("accounts-api:user-details-update-destroy", kwargs={"id": user.id})
        request = rf.get(url)
        view = views.UserDetailsUpdateDestroyView.as_view()

        # Mock
        mocker.patch.multiple(
            views.UserDetailsUpdateDestroyView,
            check_permissions=mocker.MagicMock(return_value=True),
            get_object=mocker.MagicMock(return_value=user),
        )
        # Act
        response = view(request, id=user.id).render()

        # Assert
        assert response.status_code == 200

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
    )
    @given(user=user_strategy)
    def test_delete_user_view(self, user, mocker, rf):
        # Arrange
        url = reverse("accounts-api:user-details-update-destroy", kwargs={"id": user.id})
        request = rf.delete(url)
        view = views.UserDetailsUpdateDestroyView.as_view()

        # Mock
        mocker.patch.multiple(
            views.UserDetailsUpdateDestroyView,
            check_permissions=mocker.MagicMock(return_value=True),
            get_object=mocker.MagicMock(return_value=user),
        )

        del_mock = mocker.patch.object(user, "delete")

        # Act
        response = view(request).render()

        # Assert
        assert response.status_code == 204
        del_mock.assert_called_once()


# class TestAccountResetting:
# @settings(
#     suppress_health_check=[HealthCheck.function_scoped_fixture],
#     verbosity=Verbosity.verbose,
#     max_examples=20,
# )
# @given(user=from_model(User))
# def test_send_forget_password_request_view(self, user, mocker, rf):
#     """Test sending the request to reset forgotten password for the user."""

#     # Arrange
#     payload = {
#         "email": user.email,
#     }
#     url = reverse("accounts-api:forget-password-request")
#     request = rf.post(url, data=payload)
#     view = views.ForgetPasswordRequestView.as_view()

#     # Mock
#     create_mock = mocker.patch.object(models.OTPNumber, "save")

#     # Act
#     response = view(request).render()

#     # Assert
#     assert response.status_code == 200
#     create_mock.assert_called_once()

# @settings(
#     suppress_health_check=[HealthCheck.function_scoped_fixture],
#     verbosity=Verbosity.verbose,
#     deadline=20000,
# )
# @given(user=from_model(User), new_password=st.text(min_size=8, max_size=128))
# def test_set_first_time_password_view(self, user, new_password, rf):
#     """Test setting first time password for the user."""
#     # Arrange
#     payload = {
#         "new_password": new_password,
#         "confirmed_password": new_password,
#     }
#     uri = reverse("accounts-api:first-time-password")
#     request = rf.patch(uri, data=payload, content_type="application/json")
#     request.user = user
#     view = views.FirstTimePasswordView.as_view()

#     # Act
#     response = view(request)

#     # Assert
#     assert response.status_code == 200
#     assert user.check_password(new_password)
#     assert user.is_password_changed
