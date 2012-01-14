
from django import forms
from troop.models import Troop

class TroopForm(forms.ModelForm):
    class Meta:
        model = Troop