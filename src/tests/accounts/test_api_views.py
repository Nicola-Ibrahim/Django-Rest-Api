from django.urls import reverse
from hypothesis import HealthCheck, Verbosity, given, settings
from hypothesis import strategies as st
from hypothesis.extra.django import from_model

from src.apps.accounts.api import views
from src.apps.accounts.models import models


class TestAccountsViews:
    # Define a strategy for generating users
    user_strategy: st.SearchStrategy = from_model(models.User)

    # Edit suppress_health_check for using `mocker` fixture
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
    )
    @given(users=st.lists(user_strategy, min_size=1, max_size=4))
    def test_length_of_created_users(self, users, mocker, rf):
        # Arrange
        url = reverse("accounts-api:list-users")
        request = rf.get(url)

        view = views.UserListView.as_view()

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
        url = reverse(
            "accounts-api:user-details-update-destroy", kwargs={"id": user.id}
        )
        print(url)
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
        url = reverse(
            "accounts-api:user-details-update-destroy", kwargs={"id": user.id}
        )
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
