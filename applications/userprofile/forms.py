from django import forms
from django.contrib.auth.models import User

from userprofile.models import Userprofile

class NewScoutForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        exclude = ('user',)

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    login_name = forms.CharField(max_length=50)
    
    def clean_login_name(self):
        username = self.cleaned_data['login_name']
        troop = self.cleaned_data['troop']
        username='%s_%s' % (username, troop)
        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError('A user with that login already exists.')
        except User.DoesNotExist:
            return username

        
    
    def save(self):
        cd = self.cleaned_data
        username='%s_%s' % (cd.get('login_name'), cd.get('troop'))
        
       
        try:
            user = User.objects.create_user(username, '', password='password')
            user.first_name = cd.get('first_name')
            user.last_name = cd.get('last_name')
            
            user.save()
        except Exception, e:
            raise forms.ValidationError(str(e))
        
        profile = super(NewScoutForm, self).save()
        profile.user = user
        profile.save()
        return profile
        
            
        