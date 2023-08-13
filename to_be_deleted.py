# # myapp/models.py
# from django.contrib.auth.models import User
# from django.db import models


# # A model for storing tasks that require SOD (Separation of duties) permissions
# class Task(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requested_tasks")
#     manager = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="managed_tasks",
#         null=True,
#         blank=True,
#     )
#     manager_approved = models.BooleanField(default=False)
#     infra_head = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="infra_tasks",
#         null=True,
#         blank=True,
#     )
#     infra_approved = models.BooleanField(default=False)
#     completed = models.BooleanField(default=False)


# # myapp/permissions.py
# from rest_framework.permissions import BasePermission


# # A permission class for checking if the user is the requester of the task
# class IsRequester(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.requester == request.user


# # A permission class for checking if the user is the manager of the task
# class IsManager(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.manager == request.user


# # A permission class for checking if the user is the infrastructure head of the task
# class IsInfraHead(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.infra_head == request.user


# # A permission class for checking if the task is approved by both manager and infrastructure head
# class IsApproved(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.manager_approved and obj.infra_approved


# from myapp.models import Task
# from myapp.permissions import IsApproved, IsInfraHead, IsManager, IsRequester
# from myapp.serializers import TaskSerializer

# # myapp/views.py
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# # A view for listing and creating tasks
# class TaskListCreateView(ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     # Override the perform_create method to set the requester and approvers based on the user's role
#     def perform_create(self, serializer):
#         user = self.request.user
#         role = user.role  # Assume that the user model has a role field
#         if role == "developer":
#             # Set the requester as the user and assign a manager and an infra head randomly
#             serializer.save(
#                 requester=user,
#                 manager=User.objects.filter(role="manager").order_by("?").first(),
#                 infra_head=User.objects.filter(role="infra_head").order_by("?").first(),
#             )
#         elif role == "manager":
#             # Set the requester and manager as the user and assign an infra head randomly
#             serializer.save(
#                 requester=user,
#                 manager=user,
#                 infra_head=User.objects.filter(role="infra_head").order_by("?").first(),
#             )
#         elif role == "infra_head":
#             # Set the requester and infra head as the user and assign a manager randomly
#             serializer.save(
#                 requester=user,
#                 infra_head=user,
#                 manager=User.objects.filter(role="manager").order_by("?").first(),
#             )


# # A view for retrieving, updating and deleting tasks
# class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     # Override the get_permissions method to set different permissions based on the HTTP method
#     def get_permissions(self):
#         if self.request.method == "GET":
#             # Allow anyone to view any task
#             return []
#         elif self.request.method == "PUT" or self.request.method == "PATCH":
#             # Allow only the requester to edit the task details before approval
#             return [IsRequester()]
#         elif self.request.method == "DELETE":
#             # Allow only the requester or an approver to delete the task before completion
#             return [IsRequester() | IsManager() | IsInfraHead()]

#     # Override the perform_update method to set the approval status based on the user's role
#     def perform_update(self, serializer):
#         user = self.request.user
#         role = user.role  # Assume that the user model has a role field
#         if role == "manager":
#             # Set the manager_approved field to True
#             serializer.save(manager_approved=True)
#         elif role == "infra_head":
#             # Set the infra_approved field to True
#             serializer.save(infra_approved=True)


# # A view for completing tasks
# class TaskCompleteView(RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [IsApproved]  # Require both approvals to complete the task

#     # Override the perform_update method to set the completed field to True
#     def perform_update(self, serializer):
#         serializer.save(completed=True)


# # myapp/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from myapp.models import Task


# # A signal handler for sending notifications to the approvers when a task is created or updated
# @receiver(post_save, sender=Task)
# def send_notification(sender, instance, created, **kwargs):
#     # Assume that there is a function that sends an email to a user with a subject and a message
#     from myapp.utils import send_email

#     if created:
#         # If the task is newly created, notify both the manager and the infra head
#         send_email(
#             instance.manager,
#             "New task request",
#             f"You have a new task request from {instance.requester}. Please review and approve it at /tasks/{instance.id}/",
#         )
#         send_email(
#             instance.infra_head,
#             "New task request",
#             f"You have a new task request from {instance.requester}. Please review and approve it at /tasks/{instance.id}/",
#         )
#     else:
#         # If the task is updated, check the approval status and notify accordingly
#         if instance.manager_approved and not instance.infra_approved:
#             # If the manager has approved but the infra head has not, notify the infra head
#             send_email(
#                 instance.infra_head,
#                 "Task approval pending",
#                 f"The task requested by {instance.requester} has been approved by {instance.manager}. Please review and approve it at /tasks/{instance.id}/",
#             )
#         elif not instance.manager_approved and instance.infra_approved:
#             # If the infra head has approved but the manager has not, notify the manager
#             send_email(
#                 instance.manager,
#                 "Task approval pending",
#                 f"The task requested by {instance.requester} has been approved by {instance.infra_head}. Please review and approve it at /tasks/{instance.id}/",
#             )
#         elif instance.manager_approved and instance.infra_approved:
#             # If both have approved, notify the requester
#             send_email(
#                 instance.requester,
#                 "Task approved",
#                 f"Your task has been approved by both {instance.manager} and {instance.infra_head}. You can complete it at /tasks/{instance.id}/complete/",
#             )
