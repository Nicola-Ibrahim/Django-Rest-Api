import django_filters.rest_framework as filters

from ...models.models import DeliveryWorker, Doctor, User, Warehouse


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "email": ["icontains"],
            "is_verified": ["exact"],
        }


class WarehouseFilter(filters.FilterSet):
    class Meta:
        model = Warehouse
        fields = {
            "warehouse_profile__name": ["icontains"],
            "warehouse_profile__sections__name": ["icontains", "exact"],
        }


class DoctorFilter(filters.FilterSet):
    class Meta:
        model = Doctor
        fields = {
            "doctor_profile__first_name": ["icontains"],
            "doctor_profile__last_name": ["icontains"],
            # "doctor_profile__subscription__name": ["icontains"],
        }


class DeliveryWorkerFilter(filters.FilterSet):
    class Meta:
        model = DeliveryWorker
        fields = {
            "delivery_worker_profile__first_name": ["icontains"],
            "delivery_worker_profile__last_name": ["icontains"],
            "delivery_worker_profile__is_idle": ["exact"],
        }
