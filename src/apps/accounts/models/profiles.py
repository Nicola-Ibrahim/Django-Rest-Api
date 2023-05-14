from django.db import models

from .models import (
    Admin,
    BaseAccountant,
    DeliveryWorker,
    DeliveryWorkerAccountant,
    Doctor,
    Statistician,
    Warehouse,
    WarehouseAccountant,
)
from .validators import validate_name


class BaseAccountantProfile(models.Model):
    base_accountant = models.OneToOneField(
        BaseAccountant,
        related_name="base_accountant_profile",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class DeliveryWorkerAccountantProfile(models.Model):
    delivery_worker_accountant = models.OneToOneField(
        DeliveryWorkerAccountant,
        related_name="delivery_worker_accountant_profile",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class WarehouseAccountantProfile(models.Model):
    warehouse_accountant = models.OneToOneField(
        WarehouseAccountant,
        related_name="warehouse_accountant_profile",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class AdminProfile(models.Model):
    admin = models.OneToOneField(
        Admin, related_name="admin_profile", on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class StatisticianProfile(models.Model):
    statistician = models.OneToOneField(
        Statistician,
        related_name="statistician_profile",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class WarehouseProfile(models.Model):
    warehouse = models.OneToOneField(
        Warehouse,
        related_name="warehouse_profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=200,
        validators=[validate_name],
    )
    working_hours = models.FloatField()
    profit_percentage = models.FloatField()

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.capitalize()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.ManyToManyField(WarehouseProfile, related_name="sections")

    def __str__(self) -> str:
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=200)
    Warehouse = models.ManyToManyField(WarehouseProfile, related_name="services")

    def __str__(self) -> str:
        return self.name


class DeliveryWorkerProfile(models.Model):
    delivery_worker = models.OneToOneField(
        DeliveryWorker,
        related_name="delivery_worker_profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=200, validators=[validate_name])
    last_name = models.CharField(max_length=200, validators=[validate_name])
    distance = models.FloatField(max_length=200)
    duration = models.FloatField()
    profit_percentage = models.FloatField()
    is_idle = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class DoctorProfile(models.Model):
    doctor = models.OneToOneField(
        Doctor,
        related_name="doctor_profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=200, validators=[validate_name])
    last_name = models.CharField(max_length=200, validators=[validate_name])

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name
