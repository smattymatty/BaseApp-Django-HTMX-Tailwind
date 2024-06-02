from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from BaseApp.utils import get_module_logger

from .managers import CustomUserManager


module_logger = get_module_logger("models", __file__)


class User(AbstractUser):
    """
    Custom User model
    """
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=30, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    """
    Stores further information about a user that is not needed for authentication
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    history = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile id: {self.id}"

    class Meta:
        permissions = (
            ("can_view_others", "Can view other people's Profiles"),
            ("can_edit_others", "Can edit other people's Profiles")
        )

# Signal receiver function to automatically create a profile for every new user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        if created:
            group, _ = Group.objects.get_or_create(
                name='Basic User')  # Corrected
            instance.groups.add(group)
            module_logger.debug(f"Creating Profile for {instance}")
            Profile.objects.get_or_create(user=instance)
    except Exception as e:
        module_logger.error(f"Error creating Profile: {e}")
