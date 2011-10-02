from django import forms
from django.contrib.auth.models import User

from userprofile.models import Userprofile

class NewScoutForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        exclude = ('user', 'troop')
        
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)