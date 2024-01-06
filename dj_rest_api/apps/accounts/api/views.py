from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from drf_yasg.utils import swagger_auto_schema
from lib.api.views import BaseGenericAPIView

# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from ..services import TeacherUserAndProfileBuilder
from . import permissions, responses, serializers


class UserListCreateView(
    permissions.UserListCreatePermissionMixin,
    ListModelMixin,
    CreateModelMixin,
    BaseGenericAPIView,
):
    """
    A view for listing and creating users.

    Inherits from ListModelMixin and CreateModelMixin to provide
    GET and POST methods for user listing and creation. Additionally,
    includes permission handling with UserListCreatePermissionMixin.

    Attributes:
        queryset (QuerySet): The queryset for retrieving users.
        serializer_class (Serializer): The serializer class for user data.

    Example:
        To list users, send a GET request to the endpoint.
        To create a user, send a POST request with the required data.
    """

    def get_queryset(self):
        if self.request.method == "GET":
            return get_user_model().objects.all()

        return QuerySet()

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP request method.

        Returns:
            Serializer: The serializer class for the current request method.
        """
        if self.request.method == "GET":
            return serializers.UserListSerializer

        if self.request.method == "POST":
            serializer_class = serializers.get_create_serializer(self.kwargs.get("user_type"))
            return serializer_class

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for listing users.

        Retrieves the queryset, paginates it, and serializes the data.

        Args:
            request: The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The paginated user data response.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return responses.UserListResponse().with_data(users_data=serializer.data)

    @swagger_auto_schema(request_body=serializers.StudentUserCreateSerializer)
    def post(self, request, *args, **kwargs) -> Response:
        """
        Handles POST requests for creating users.

        Validates the request data, saves the user, and returns a response.

        Args:
            request: The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The user creation response.
        """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        TeacherUserAndProfileBuilder.construct(user_data=serializer.data)

        return responses.UserCreateResponse().with_data(user_data=serializer.data)


class UserDetailsUpdateDestroyView(
    permissions.UserDetailsUpdateDestroyPermissionMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    BaseGenericAPIView,
):
    """
    A view for retrieving, updating, and deleting user details.

    Inherits from RetrieveModelMixin, UpdateModelMixin, and DestroyModelMixin
    to provide GET, PUT, PATCH, and DELETE methods for user details.
    Additionally, includes permission handling with BasePermissionMixin.

    Attributes:
        queryset (QuerySet): The queryset for retrieving users.
        lookup_field (str): The lookup field for retrieving users by ID.

    Example:
        To retrieve user details, send a GET request to the endpoint with the user's ID.
        To update user details, send a PUT or PATCH request with the updated data.
        To delete a user, send a DELETE request with the user's ID.
    """

    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def get_serializer_class(self, *args, **kwargs):
        """
        Returns the appropriate serializer class based on the HTTP request method.

        Returns:
            Serializer: The serializer class for the current request method.
        """
        serializer_class = None

        if self.request.method == "GET":
            serializer_class = serializers.UserDetailsSerializer

        elif self.request.method in ["PUT", "PATCH"]:
            user = self.get_object()
            serializer_class = serializers.get_update_serializer(user_type=user.type)

        return serializer_class

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handles GET requests for retrieving user details.

        Retrieves the user, serializes the data, and returns the response.

        Args:
            request: The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The user details response.
        """
        user = self.get_object()
        serializer = self.get_serializer(instance=user, context={"request": request})
        return responses.UserDetailsResponse().with_data(serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Handles PUT requests for updating user details.

        Validates the request data, performs the update, and returns the response.

        Args:
            request: The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The user update response.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            partial=partial,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return responses.UserUpdateResponse().with_data(user_data=serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        Handles PATCH requests for partially updating user details.

        Validates the request data, performs the partial update, and returns the response.

        Args:
            request: The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The user update response.
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return responses.UserUpdateResponse().with_data(user_data=serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Handles DELETE requests for deleting a user.

        Performs the deletion and returns the response.

        Args:
            request: The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The user deletion response.
        """
        user = self.get_object()
        self.perform_destroy(user)
        return responses.UserDestroyResponse()


class VerifyUserAccount(
    permissions.VerifyUserAccountPermissionMixin,
    BaseGenericAPIView,
):
    """Verify the user by the token send it to the email"""

    serializer_class = serializers.AccountVerificationSerializer

    def get(self, request):
        serializer = self.get_serializer(request.GET.get("token"), context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return responses.ActivatedAccount()
