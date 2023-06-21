"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..api.permissions.permissions import PermissionGroupsName
from .models import Student, Teacher


@receiver(post_save, sender=Teacher)
def assign_group(sender, instance, **kwargs):
    """Assign permission group to the user"""

    try:
        # Get the warehouse permission groups
        perm_group = Group.objects.get(name=PermissionGroupsName.TEACHER_GROUP.value)

    except Group.DoesNotExist:
        pass

    else:
        # Assign the new instance to the group
        perm_group.user_set.add(instance)  # type:ignore


@receiver(post_save, sender=Student)
def assign_group(sender, instance, **kwargs):  # noqa:F811
    """Assign permission group to the user"""

    try:
        # Get the warehouse permission groups
        perm_group = Group.objects.get(name=PermissionGroupsName.STUDENT_GROUP.value)

    except Group.DoesNotExist:
        pass
    else:
        # Assign the new instance to the group
        perm_group.user_set.add(instance)
