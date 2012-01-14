
from django import forms
from troop.models import Troop

class TroopForm(forms.ModelForm):
    class Meta:
        model = Troop
        exclude = ('council','calendar')
        
    council_name = forms.CharField(max_length=255)