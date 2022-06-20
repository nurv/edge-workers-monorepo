from django import forms

from datasets.models import Dataset
from training.models import MLModel, MLModelDataset, InputFeatures, OutputFeatures, MLModelVersion


class MLModelForm(forms.ModelForm):
    class Meta:
        model = MLModel
        fields = ["name", "bucket"]
        help_texts = {
            'bucket': 'Where the model assets should be stored',
        }

class InputFeatureForm(forms.ModelForm):
    model = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=MLModel.objects.all())

    class Meta:
        model = InputFeatures
        fields = ["name", "type", "model"]


class OutputFeatureForm(forms.ModelForm):
    model = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=MLModel.objects.all())

    class Meta:
        model = OutputFeatures
        fields = ["name", "type", "model"]


class MLModelDatasetForm(forms.ModelForm):
    dataset = forms.ModelChoiceField(label="Snapshot", queryset=Dataset.objects.all())
    model = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=MLModel.objects.all())

    class Meta:
        model = MLModelDataset
        fields = ["dataset", "model"]


class MLModelVersionForm(forms.ModelForm):
    dataset = forms.ModelChoiceField(label="Data Snapshot", queryset=MLModelDataset.objects.all())
    model = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=MLModel.objects.all())

    class Meta:
        model = MLModelVersion
        fields = ["dataset", "model"]

