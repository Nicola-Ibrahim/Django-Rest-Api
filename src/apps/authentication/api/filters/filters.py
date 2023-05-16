import django_filters.rest_framework as filters

from ...models.models import DeliveryWorker, Doctor, User, Warehouse


class UserFilter(filters.FilterSet):
    """A FilterSet subclass for filtering User model instances.

    This class defines the fields and lookup expressions that can be used to filter
    the User queryset by email and verification status.

    Attributes:
        Meta: A class that contains the model and fields information for the FilterSet.
    """

    class Meta:
        model = User
        fields = {
            "email": ["icontains"],  # Case-insensitive containment match
            "is_verified": ["exact"],  # Exact match
        }


class WarehouseFilter(filters.FilterSet):
    """A FilterSet subclass for filtering Warehouse model instances.

    This class defines the fields and lookup expressions that can be used to filter
    the Warehouse queryset by warehouse profile name and section name.

    Attributes:
        Meta: A class that contains the model and fields information for the FilterSet.
    """

    class Meta:
        model = Warehouse
        fields = {
            "warehouse_profile__name": ["icontains"],  # Case-insensitive containment match
            "warehouse_profile__sections__name": [
                "icontains",
                "exact",
            ],  # Case-insensitive containment match or exact match
        }


class DoctorFilter(filters.FilterSet):
    """A FilterSet subclass for filtering Doctor model instances.

    This class defines the fields and lookup expressions that can be used to filter
    the Doctor queryset by doctor profile first name, last name and subscription name.

    Attributes:
        Meta: A class that contains the model and fields information for the FilterSet.
    """

    class Meta:
        model = Doctor
        fields = {
            "doctor_profile__first_name": ["icontains"],  # Case-insensitive containment match
            "doctor_profile__last_name": ["icontains"],  # Case-insensitive containment match
            # "doctor_profile__subscription__name": ["icontains"],  # Case-insensitive containment match
        }


class DeliveryWorkerFilter(filters.FilterSet):
    """A FilterSet subclass for filtering DeliveryWorker model instances.

    This class defines the fields and lookup expressions that can be used to filter
    the DeliveryWorker queryset by delivery worker profile first name, last name and idle status.

    Attributes:
        Meta: A class that contains the model and fields information for the FilterSet.
    """

    class Meta:
        model = DeliveryWorker
        fields = {
            "delivery_worker_profile__first_name": ["icontains"],  # Case-insensitive containment match
            "delivery_worker_profile__last_name": ["icontains"],  # Case-insensitive containment match
            "delivery_worker_profile__is_idle": ["exact"],  # Exact match
        }
