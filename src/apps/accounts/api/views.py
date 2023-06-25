from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.apps.core import mailers
from src.apps.core.api.views import BaseGenericApiView

from . import exceptions as accounts_exceptions
from . import responses as accounts_responses
from .filters.mixins import FilterMixin
from .permissions import mixins as permissions_mixin
from .queryset.mixins import InUserTypeQuerySetMixin, QueryParamUserTypeSerializerMixin
from .serializers.mixins import (
    InUserTypeSerializerMixin,
    QueryParamUserTypeQuerySetMixin,
)
from .serializers.serializers import AccountVerificationSerializer, UserSerializer


class VerifyAccount(BaseGenericApiView):
    """Verify the user by the token send it to the email"""

    permission_classes = (AllowAny,)
    serializer_class = AccountVerificationSerializer

    def get(self, request):
        serializer = self.get_serializer(request.GET.get("token"), context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return accounts_responses.ActivatedAccount()


class UserDetailsView(
    InUserTypeQuerySetMixin,
    InUserTypeSerializerMixin,
    permissions_mixin.BasePermissionMixin,
    generics.RetrieveAPIView,
):
    """
    Class based view to Get User Details using Token Authentication
    """

    def get(self, request, *args, **kwargs) -> Response:
        """Override get method to obtain details depending on login user type

        Args:
            request: incoming request

        Returns:
            Response: rest framework response with user data
        """

        serializer = self.get_serializer(request.user, context={"request": request})
        return Response(serializer.data)


class UserUpdateView(
    InUserTypeQuerySetMixin,
    InUserTypeSerializerMixin,
    permissions_mixin.BasePermissionMixin,
    generics.UpdateAPIView,
):
    serializer_class = UserSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.user.id}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserDeleteView(
    InUserTypeQuerySetMixin,
    InUserTypeSerializerMixin,
    generics.DestroyAPIView,
):
    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.user.id}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def destroy(self, request, *args, **kwargs):
        """Override destroy method to handle deleting for multiple users

        Args:
            request: incoming request
        """

        # Get the users to be deleted
        ids = request.data["ids"]

        # Get the user who perform the delete action
        _ = self.get_object()

        # Execute delete the ids
        users_deleted = self.perform_destroy(ids)

        msg = {"details": f"Deleted the users: {users_deleted}"}
        return Response(data=msg, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, ids):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"pk__in": ids}
        users_deleted = queryset.filter(**filter_kwargs).delete()
        return users_deleted


class UsersListCreateView(
    QueryParamUserTypeQuerySetMixin,
    QueryParamUserTypeSerializerMixin,
    # FilterMixin,
    permissions_mixin.ListCreateUserPermissionMixin,
    ListModelMixin,
    CreateModelMixin,
    BaseGenericApiView,
):

    """View for listing and adding a new user"""

    queryset = get_user_model().objects.all()

    def post(self, request, *args, **kwargs) -> Response:
        """Override post method to control the behavior of inserting a new user
        Returns:
            Response: rest framework response with user data
        """
        user_data = request.data
        serializer = self.get_serializer(data=user_data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create random password for user
        password = get_user_model().objects.make_random_password()
        user.set_password(password)
        user.save(update_fields=["password"])

        # Send welcome email
        # mailers.RegisterMailer(
        #     to_email=user.email, password=password
        # ).send_email()
        mailers.VerificationMailer(token=user.tokens()["access"], to_emails=[user.email], request=request)
        return accounts_responses.UserCreateResponse()


class UserDetailsUpdateDestroyView(
    permissions_mixin.BasePermissionMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    BaseGenericApiView,
):
    queryset = get_user_model().objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            if self.request.user.is_granted_group:
                return UserAdminUpdateSerializer
            else:
                return UserNotAdminUpdateSerializer

        return UserDetailSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly." % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = queryset.filter(**filter_kwargs)
        if not obj.exists():
            raise accounts_exceptions.UserNotExists()

        obj = obj.first()

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return accounts_responses.UserUpdateResponse()

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return accounts_responses.UserDestroyResponse()
