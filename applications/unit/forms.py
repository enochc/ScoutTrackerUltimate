
from django import forms
from unit.models import Unit

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ('council','calendar')

    user_role = forms.IntegerField()
    council_name = forms.CharField(max_length=255)
    