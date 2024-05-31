from django.db.models.signals import post_save
from django.dispatch import receiver

from BaseApp.utils import get_module_logger

from .models import BlogCategory

logger = get_module_logger("signals", __file__)


@receiver(post_save, sender=BlogCategory)
def print_category_name(sender, instance, created, **kwargs):
    if created:
        logger.success(f"Category created: {instance.name}")
