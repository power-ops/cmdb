from django import forms
from exampleapp import models


class ExampleForm(forms.ModelForm):
    class Meta:
        model = models.ExampleModel
        fields = ['uuid', 'CreateDate', 'Enabled']
