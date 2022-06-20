import uuid

from django.db import models

# Create your models here.
from django.utils import timezone


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    name = models.CharField("Name", max_length=1024)
    query = models.TextField("Query", blank=True)
    mean = models.FloatField("Mean")
    std = models.FloatField("Standard Deviation")
    content = models.TextField("Content", blank=True)