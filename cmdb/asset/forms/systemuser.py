from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from asset import models


class SystemUserForm(forms.ModelForm):
    Protocols = forms.ModelMultipleChoiceField(
        queryset=models.Protocol.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Protocols'),
            is_stacked=False,
        )
    )
    Password = forms.CharField(required=False)
    KeyFile = forms.FileField(label=_('KeyFile'), required=False)

    # def __init__(self, *args, **kwargs):
    #     super(SystemUserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.SystemUser
        fields = ['Name', 'Username', 'Password', 'KeyFile', 'Protocols', 'Enabled']

    def save(self, commit=True):
        instance = super(SystemUserForm, self).save(commit=False)
        try:
            instance.Key = self.cleaned_data['KeyFile'].read()
        except:
            pass
        return instance
