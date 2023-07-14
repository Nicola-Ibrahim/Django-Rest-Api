"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""
import functools

from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from ..api.permissions.permissions import PermissionGroupsName
from . import models, profiles

# @receiver(post_save, sender=models.Teacher)
# def assign_group(sender, instance, **kwargs):
#     """Assign permission group to the user"""

#     try:
#         # Get the warehouse permission groups
#         perm_group = Group.objects.get(name=PermissionGroupsName.TEACHER_GROUP.value)

#     except Group.DoesNotExist:
#         pass

#     else:
#         # Assign the new instance to the group
#         perm_group.user_set.add(instance)  # type:ignore


# @receiver(post_save, sender=models.Student)
# def assign_group(sender, instance, **kwargs):  # noqa:F811
#     """Assign permission group to the user"""

#     try:
#         # Get the warehouse permission groups
#         perm_group = Group.objects.get(name=PermissionGroupsName.STUDENT_GROUP.value)

#     except Group.DoesNotExist:
#         pass
#     else:
#         # Assign the new instance to the group
#         perm_group.user_set.add(instance)


@receiver(post_save, sender=models.Admin, dispatch_uid="admin_post_save")
def create_admin_profile(sender, instance, created, **kwargs):
    if created:
        profiles.AdminProfile.objects.create(admin=instance)


@receiver(post_save, sender=models.Student, dispatch_uid="student_post_save")
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        profiles.StudentProfile.objects.create(student=instance)


@receiver(post_save, sender=models.Teacher, dispatch_uid="teacher_post_save")
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        profiles.TeacherProfile.objects.create(teacher=instance)


def signal_wrapper(signal, sender, receiver, dispatch_uid):
    """Wrapper to disconnect signal and reconnect after finish executing func"""

    def decorator(func):
        # Define a modified version of the original function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Disconnect the signal before calling the original function
            signal.disconnect(sender=sender, dispatch_uid=dispatch_uid)

            # Call the original function and store the result
            result = func(*args, **kwargs)

            # Reconnect the signal after calling the original function
            signal.connect(sender=sender, receiver=receiver, dispatch_uid=dispatch_uid)

            # Return the result of the original function
            return result

        # Return the modified version of the original function
        return wrapper

    # Return the decorator
    return decorator
