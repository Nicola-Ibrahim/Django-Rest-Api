"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..api.permissions.permissions import PermissionGroupsName
from .models import Doctor, Warehouse


@receiver(post_save, sender=Warehouse)
def assign_group(sender, instance, **kwargs):
    """Assign permission group to the user"""

    try:
        # Get the warehouse permission groups
        perm_group = Group.objects.get(name=PermissionGroupsName.WAREHOUSE_GROUP.value)

    except Group.DoesNotExist:
        pass

    else:
        # Assign the new instance to the group
        perm_group.user_set.add(instance)  # type:ignore


@receiver(post_save, sender=Doctor)
def assign_group(sender, instance, **kwargs):  # noqa:F811
    """Assign permission group to the user"""

    try:
        # Get the warehouse permission groups
        perm_group = Group.objects.get(name=PermissionGroupsName.DOCTOR_GROUP.value)

    except Group.DoesNotExist:
        pass
    else:
        # Assign the new instance to the group
        perm_group.user_set.add(instance)
