from rest_framework import serializers

from apps.core.api.serializers import BaseModelSerializer

from ...models.profiles import DeliveryWorkerProfile, DoctorProfile, WarehouseProfile


class WarehouseProfileSerializer(BaseModelSerializer):
    class Meta:
        model = WarehouseProfile
        fields = [
            "name",
            "working_hours",
            "profit_percentage",
            "warehouse",
        ]

        extra_kwargs = {
            "warehouse": {"write_only": True},
        }


class DoctorProfileSerializer(BaseModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["first_name", "last_name", "doctor"]

        extra_kwargs = {
            "doctor": {"write_only": True},
        }


class DeliveryWorkerProfileSerializer(BaseModelSerializer):
    class Meta:
        model = DeliveryWorkerProfile
        fields = "__all__"

        extra_kwargs = {
            "delivery_worker": {"write_only": True},
        }
