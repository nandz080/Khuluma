from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Creating profile for user: {instance.username}")
        Profile.objects.create(
            user=instance, 
            username=instance.username, 
            first_name=instance.first_name, 
            last_name=instance.last_name, 
            profile_picture=instance.profile_picture
        )
    else:
        logger.info(f"User profile already exists for user: {instance.username}")

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        logger.info(f"Saving profile for user: {instance.username}")
        instance.profile.save()

