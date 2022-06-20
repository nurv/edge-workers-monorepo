import json
import uuid

from django.db import models
from django.utils import timezone


class Function(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    name = models.TextField("Name")
    code = models.TextField("Code", blank=True)

    def code_js(self):
        return json.dumps(self.code);
