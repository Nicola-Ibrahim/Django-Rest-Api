from django.urls import reverse

from src.apps.accounts.api import views


class TestAccountsViews:
    def test_list_users_view(self, mocker, users, rf):
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
        assert len(response.data["data"]) == 3

    def test_retrieve_user_view(self, one_user, mocker, rf):
        # Arrange
        url = reverse(
            "accounts-api:user-details-update-destroy", kwargs={"id": one_user.id}
        )
        request = rf.get(url)
        view = views.UserDetailsUpdateDestroyView.as_view()

        # Mock
        mocker.patch.multiple(
            views.UserDetailsUpdateDestroyView,
            check_permissions=mocker.MagicMock(return_value=True),
            get_queryset=mocker.MagicMock(return_value=one_user),
        )
        # Act
        response = view(request, id=one_user.id).render()

        # Assert
        assert response.status_code == 200

    def test_delete_user_view(self, one_user, mocker, rf):
        # Arrange
        url = reverse(
            "accounts-api:user-details-update-destroy", kwargs={"id": one_user.id}
        )
        request = rf.delete(url)
        view = views.UserDetailsUpdateDestroyView.as_view()

        # Mock
        mocker.patch.multiple(
            views.UserDetailsUpdateDestroyView,
            check_permissions=mocker.MagicMock(return_value=True),
            get_object=mocker.MagicMock(return_value=one_user),
        )

        del_mock = mocker.patch.object(one_user, "delete")

        # Act
        response = view(request).render()

        # Assert
        assert response.status_code == 204
        del_mock.assert_called_once()
