import uuid

from django.db import models
from django.utils import timezone

from datasets.models import Dataset
from training.tasks import train

class MLModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    name = models.CharField("Name", max_length=1024)
    bucket = models.CharField("Bucket", blank=True, default="", max_length=1024)

    def get_config(self):
        input_features = []
        for inputs in self.inputs.all():
            input_features.append(inputs.get_config())

        output_features = []
        for outputs in self.outputs.all():
            output_features.append(outputs.get_config())

        return {
            "input_features": input_features,
            "output_features": output_features,
        }

FEATURE_TYPE_CHOICES = (
    ("binary", "Binary"),
    ("numerical", "Numerical"),
    ("category", "Category"),
    ("bag", "Bag"),
    ("sequence", "Sequence"),
    ("vector", "Vector"),
    ("audio", "Audio"),
    ("date", "Date"),
    ("h3", "H3"),
    ("image", "Image"),
    ("timeseries", "Time Series"),
)


class InputFeatures(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    name = models.CharField("Name", max_length=1024)
    type = models.CharField("Type", choices=FEATURE_TYPE_CHOICES, max_length=1024)
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name="inputs")

    def get_config(self):
        return {
            "name": self.name,
            "type": self.type,
            'encoder': 'rnn',
            'embedding_size': 32,
            'state_size': 32
        }

class OutputFeatures(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    name = models.CharField("Name", max_length=1024)
    type = models.CharField("Type", choices=FEATURE_TYPE_CHOICES, max_length=1024)
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name="outputs")

    def get_config(self):
        return {
            "name": self.name,
            "type": self.type,
        }

class MLModelDataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    dataset = models.ForeignKey(Dataset, null=True, on_delete=models.CASCADE)
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)


class MLModelVersion(models.Model):
    STATUS_CHOICES=(
        ("wait", "Wait to start"),
        ("training", "Training"),
        ("optimizing", "Optimizing"),
        ("error", "Error"),
        ("finished", "Finished"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    trained = models.DateTimeField(blank=True, null=True)
    status = models.CharField("Status", default="wait", choices=STATUS_CHOICES, max_length=50)
    dataset = models.ForeignKey(MLModelDataset, on_delete=models.CASCADE)
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name="versions")
    evaluation_result = models.TextField("Evaluation Result")

    def train(self):
        train.delay(self.id)
