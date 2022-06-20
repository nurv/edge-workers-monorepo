import uuid

from django.db import models
from django.utils import timezone


class Bucket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    name = models.CharField("Name", max_length=1024)

