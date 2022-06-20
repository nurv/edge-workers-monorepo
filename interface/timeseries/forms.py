from django import forms


class TSDBForm(forms.Form):
    name = forms.CharField()

