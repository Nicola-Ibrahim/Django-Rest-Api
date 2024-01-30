from apps.accounts import models, services
from core.api.serializers import BaseModelSerializer
from core.api.views import BaseGenericAPIView
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings

from . import filters, permissions, responses, serializers


class UserListCreateView(
    ListModelMixin,
    CreateModelMixin,
    BaseGenericAPIView,
):
    """
    A view for listing and creating users.

    Inherits from ListModelMixin and CreateModelMixin to provide
    GET and POST methods for user listing and creation. Additionally,

    Example:
        To list users, send a GET request to the endpoint.
        To create a user, send a POST request with the required data.
    """

    permission_classes = [permissions.UserListCreatePermission]
    filterset_class = filters.UserFilter

    def get_queryset(self):
        if self.request.method == "GET":
            return get_user_model().objects.all()

        return QuerySet()

    def get_serializer_class(self) -> BaseModelSerializer:
        """
        Returns the appropriate serializer class based on the HTTP request method.

        Returns:
            Serializer: The serializer class for the current request method.
        """

        serializer_classes = {
            "GET": serializers.UserListSerializer,
            "POST": serializers.UserCreateSerializer,
        }

        return serializer_classes.get(self.request.method, None)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for listing users.

        Retrieves the queryset, paginates it, and serializes the data.

        Returns:
            Response: The paginated user data response.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return responses.UserListAPIResponse(serializer.data)

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handles POST requests for creating users.

        Validates the request data, saves the user, and returns a response.

        Returns:
            Response: The user creation response.
        """

        # Validate the user data
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # Create a user
        services.create_user(data=serializer.data)

        headers = self.get_success_headers(serializer.data)

        return responses.UserCreatedAPIResponse(data=serializer.data, headers=headers)

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class UserDetailsUpdateDestroyView(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    BaseGenericAPIView,
):
    """
    A view for retrieving, updating, and deleting user details.

    Inherits from RetrieveModelMixin, UpdateModelMixin, and DestroyModelMixin
    to provide GET, PUT, PATCH, and DELETE methods for user details.

    Attributes:
        queryset (QuerySet): The queryset for retrieving users.
        lookup_field (str): The lookup field for retrieving users by ID.

    Example:
        To retrieve user details, send a GET request to the endpoint with the user's ID.
        To update user details, send a PUT or PATCH request with the updated data.
        To delete a user, send a DELETE request with the user's ID.
    """

    permission_classes = [permissions.UserDetailsUpdateDestroyPermission]
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def get_serializer_class(self, *args, **kwargs) -> BaseModelSerializer:
        """
        Returns the appropriate serializer class based on the HTTP request method.

        Returns:
            Serializer: The serializer class for the current request method.
        """

        serializer_classes = {
            "GET": serializers.UserDetailsSerializer,
            "PUT": serializers.UserUpdateSerializer,
            "PATCH": serializers.UserUpdateSerializer,
        }

        return serializer_classes.get(self.request.method, None)

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handles GET requests for retrieving user details.

        Retrieves the user, serializes the data, and returns the response.


        Returns:
            Response: The user details response.
        """
        user = self.get_object()
        serializer = self.get_serializer(instance=user, context={"request": request})
        return responses.UserDetailsAPIResponse(data=serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Handles PUT requests for updating user details.

        Validates the request data, performs the update, and returns the response.

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

        user_crud = models.get_crud_instance(user_type=serializer.data.get("user_type"))
        user_crud.create_user(data=serializer.data)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return responses.UserUpdateAPIResponse(user_data=serializer.data)

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

        return responses.UserUpdateAPIResponse(user_data=serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        Handles DELETE requests for deleting a user.

        Performs the deletion and returns the response.

        Returns:
            Response: The user deletion response.
        """
        user = self.get_object()
        self.perform_destroy(user)
        return responses.UserDestroyAPIResponse()


class VerifyUserAccount(BaseGenericAPIView):
    """Verify the user by the token send it to the email"""

    permission_classes = [AllowAny]
    serializer_class = serializers.AccountVerificationSerializer

    def get(self, request):
        serializer = self.get_serializer(request.GET.get("token"), context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = services.get_user_from_access_token(token=serializer.data.get("token"))
        services.verify_user_account(user=user)

        return responses.ActivatedAccountAPIResponse()


class ProfileDetailsUpdateView(RetrieveModelMixin, UpdateModelMixin, BaseGenericAPIView):
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP request method.

        Returns:
            Serializer: The serializer class for the current request method.
        """

        if self.request.method == "GET":
            user = self.get_object()
            serializer_class = serializers.get_profile_serializer(user_type=user.type.lower())
            return serializer_class

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handles GET requests for retrieving user details.

        Retrieves the user, serializes the data, and returns the response.

        Returns:
            Response: The user details response.
        """
        user = self.get_object()
        serializer = self.get_serializer(instance=user, context={"request": request})
        return responses.UserDetailsAPIResponse(user_data=serializer.data)
