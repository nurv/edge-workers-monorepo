from django.forms import ModelForm

from .models import Dataset


class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = ["name", "query"]
