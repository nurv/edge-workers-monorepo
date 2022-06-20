from django.forms import ModelForm

from buckets.models import Bucket


class BucketForm(ModelForm):
    class Meta:
        model = Bucket
        fields = ["name"]
