from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import BlogPost
import logging

logger = logging.getLogger('core')


@receiver(post_delete, sender=BlogPost)
def update_blog_list_count(sender, instance, **kwargs):
    if instance.status == 1:
        blog_list_count = cache.get('blog_list_count', 0) - 1
        if blog_list_count > 0:  # only update if chache had already been set
            cache.set('blog_list_count', blog_list_count, 30)


@receiver(post_save, sender=BlogPost)
def update_blog_list_count(sender, instance, **kwargs):
    if instance.status == 1:
        blog_list_count = cache.get('blog_list_count', 0)
        if blog_list_count > 0:
            cache.set('blog_list_count', blog_list_count + 1, 30)
