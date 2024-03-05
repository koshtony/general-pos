from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Stocks


@receiver(post_delete, sender=Stocks, dispatch_uid='post_deleted')
def object_post_delete_handler(sender, **kwargs):
     cache.delete('stocks')


@receiver(post_save, sender=Stocks, dispatch_uid='posts_updated')
def object_post_save_handler(sender, **kwargs):
    cache.delete('stocks')