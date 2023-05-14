import django_filters.rest_framework as filters

from ..models.models import DeliveryWorker, Doctor, User, Warehouse
from .exceptions import (
    UserFilterNotFound,
    UserModelNotFound,
    UserSerializerNotFound,
)
from .filters.filters import (
    DeliveryWorkerFilter,
    DoctorFilter,
    UserFilter,
    WarehouseFilter,
)
from .serializers.serializers import (
    DeliveryWorkerUserSerializer,
    DoctorUserSerializer,
    UserSerializer,
    WarehouseUserSerializer,
)


class UserTypeModelFactory:
    def get_suitable_model(self, type: str) -> User:  # type:ignore # noqa: A002
        """Get the suitable serializer for user relying on its type

        Args:
            type (str): the type of model

        Raises:
            UserModelNotFound: model not found error

        Returns:
            User: model for register a user
        """

        models_classes = {
            "user": User,
            "admin": User,
            "warehouse": Warehouse,
            "doctor": Doctor,
            "delivery_worker": DeliveryWorker,
        }
        model = models_classes.get(type, None)

        if not model:
            raise UserModelNotFound()

        return model


class UserTypeSerializerFactory:
    def get_suitable_serializer(self, type: str) -> UserSerializer:  # noqa: A002
        """Get the suitable serializer for user relying on its type

        Args:
            type (str): the type of serializer

        Raises:
            UserSerializerNotFound: serializer not found error

        Returns:
            UserSerializer: serializer for register a user
        """

        serializers_classes = {
            "user": UserSerializer,
            "admin": UserSerializer,
            "warehouse": WarehouseUserSerializer,
            "doctor": DoctorUserSerializer,
            "delivery_worker": DeliveryWorkerUserSerializer,
        }

        serializer = serializers_classes.get(type, None)

        if not serializer:
            raise UserSerializerNotFound()

        return serializer


class UserTypeFilterFactory(filters.DjangoFilterBackend):
    def get_suitable_filter(self, type: str) -> filters.FilterSet:  # noqa: A002
        """This a factory method to get the suitable filter for user registration

        Args:
            type (str): the type of filter

        Raises:
            UserFilterNotFound: filter not found error

        Returns:
            FilterSet: filter compatible with user type
        """

        filters_classes = {
            "user": UserFilter,
            "warehouse": WarehouseFilter,
            "doctor": DoctorFilter,
            "delivery_worker": DeliveryWorkerFilter,
        }

        filter_ = filters_classes.get(type, None)

        if not filter_:
            raise UserFilterNotFound()

        return filter_

    def get_filterset_class(self, view, queryset=None):
        """
        Return the `FilterSet` class used to filter the queryset.
        """
        filterset_class = self.get_suitable_filter(view.kwargs["user_type"])
        filterset_fields = getattr(view, "filterset_fields", None)  # type: ignore # noqa: F841

        if filterset_class:
            filterset_model = filterset_class._meta.model  # type: ignore # noqa: E261

            # FilterSets do not need to specify a Meta class
            if filterset_model and queryset is not None:
                assert issubclass(
                    queryset.model, filterset_model
                ), "FilterSet model {} does not match queryset model {}".format(
                    filterset_model,
                    queryset.model,
                )

            return filterset_class
