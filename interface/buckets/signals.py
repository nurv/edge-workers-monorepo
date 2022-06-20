import os
import shutil

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from buckets.models import Bucket


@receiver(post_save, sender=Bucket)
def create_bucket(sender, instance, **kwargs):
    if instance.name:
        path = os.path.join(settings.ROOT_BUCKET, instance.name)
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)


@receiver(post_delete, sender=Bucket)
def delete_bucket(sender, instance, **kwargs):
    if instance.name:
        path = os.path.join(settings.ROOT_BUCKET, instance.name)
        isExist = os.path.exists(path)
        if isExist:
            shutil.rmtree(path)

