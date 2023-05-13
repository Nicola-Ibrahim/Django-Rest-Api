from rest_framework import serializers

from ...profiles import DeliveryWorkerProfile, DoctorProfile, WarehouseProfile


class WarehouseProfileSerializer(serializers.ModelSerializer):
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


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ["first_name", "last_name", "doctor"]

        extra_kwargs = {
            "doctor": {"write_only": True},
        }


class DeliveryWorkerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryWorkerProfile
        fields = "__all__"

        extra_kwargs = {
            "delivery_worker": {"write_only": True},
        }
