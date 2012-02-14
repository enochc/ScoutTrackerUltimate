
from django import forms
from troop.models import Troop

class TroopForm(forms.ModelForm):
    class Meta:
        model = Troop
        exclude = ('council','calendar')

    user_role = forms.IntegerField()
    council_name = forms.CharField(max_length=255)