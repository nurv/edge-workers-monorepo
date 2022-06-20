from django.forms import ModelForm

from .models import Function


class FunctionNameForm(ModelForm):
    class Meta:
        model = Function
        fields = ["name"]
