from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models.models import Profile, User

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(pre_save, sender=Profile)
# def update_if_exists(sender, instance, **kwargs):
#     if Profile.objects.filter(user=instance.user).exists():
#         Profile.objects.filter(user=instance.user).delete()
