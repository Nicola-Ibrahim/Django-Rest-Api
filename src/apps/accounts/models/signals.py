"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""
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


@receiver(post_save, sender=models.Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        if not profiles.StudentProfile.objects.filter(student=instance).exists():
            profiles.StudentProfile.objects.create(student=instance)


@receiver(post_save, sender=models.Teacher)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        if not profiles.TeacherProfile.objects.filter(teacher=instance).exists():
            profiles.TeacherProfile.objects.create(teacher=instance)


# @receiver(pre_save, sender=models.Teacher)
# def update_if_exists(sender, instance, **kwargs):
#     if models.Teacher.objects.filter(user=instance.user).exists():
#         models.Teacher.objects.filter(user=instance.user).delete()
