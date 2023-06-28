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
from .queryset.mixins import InUserTypeQuerySetMixin, QueryParamUserTypeQuerySetMixin
from .serializers import factories as serializer_factory
from .serializers.mixins import (
    InUserTypeSerializerMixin,
    QueryParamUserTypeSerializerMixin,
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


class UserListView(
    # FilterMixin,
    # permissions_mixin.ListCreateUserPermissionMixin,
    ListModelMixin,
    BaseGenericApiView,
):

    """View for listing and adding a new user"""


class UserListCreateView(
    QueryParamUserTypeQuerySetMixin,
    # FilterMixin,
    # permissions_mixin.ListCreateUserPermissionMixin,
    ListModelMixin,
    CreateModelMixin,
    BaseGenericApiView,
):

    """View for creating a user.
    It supports creating different user types.
    """

    def get_serializer_class(self):
        """
        Get the appropriate serializer depending on the url user_type param
        """
        serializer_class = serializer_factory.get_serializer(self.request.GET.get("user_type"))
        return serializer_class

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs) -> Response:
        # Get appropriate serializer depending on the user_type kwarg
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # Create the user
        user = serializer.save()

        # Send welcome email
        # mailers.RegisterMailer(
        #     to_email=user.email, password=password
        # ).send_email()
        mailers.VerificationMailer(token=user.tokens()["access"], to_emails=[user.email], request=request)
        return accounts_responses.UserCreateResponse()


class UserDetailsUpdateDestroyView(
    # permissions_mixin.BasePermissionMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    BaseGenericApiView,
):
    queryset = get_user_model().objects.all()
    lookup_field = "id"

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
        user_obj = queryset.filter(**filter_kwargs)
        if not user_obj.exists():
            raise accounts_exceptions.UserNotExists()

        user_obj = user_obj.first()

        # May raise a permission denied
        self.check_object_permissions(self.request, user_obj)

        return user_obj

    def get_serializer(self, *args, **kwargs):
        serializer_class = serializer_factory.get_serializer(user_type=self.request.user.type)
        return serializer_class

    def get(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(request.user, context={"request": request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return accounts_responses.UserUpdateResponse()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return accounts_responses.UserDestroyResponse()
