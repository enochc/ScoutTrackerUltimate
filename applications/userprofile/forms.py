import datetime

from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import date as _date

from userprofile.models import Userprofile

class NewScoutForm(forms.ModelForm):

        
    class Meta:
        model = Userprofile
        exclude = ('user',)
    
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    login_name = forms.CharField(max_length=50)
    bd_string = forms.CharField(max_length=50, required=False)
    
    bd_date = None
    
    def clean_bd_string(self):
        bd_string = self.cleaned_data['bd_string']
        bd = datetime.datetime.strptime(bd_string, '%b %d, %Y')
        self.bd_date = bd
        return bd_string    
    
    def clean_login_name(self):
        username = self.cleaned_data['login_name']
        troop = self.cleaned_data['troop']
        username='%s_%s' % (username, troop)
        try:
            u = User.objects.get(username=username)
            if u != self.instance.user:
                #if u.profile != self.instance:
                raise forms.ValidationError('A user with that login already exists.')
            else:
                return username
        except User.DoesNotExist:
            return username

        
    
    def save(self, *args, **kwargs):
        cd = self.cleaned_data
        username='%s' % (cd.get('login_name'))
        if not self.instance.pk:
            try:
                user = User.objects.create_user(username, '', password='password')
            except Exception, e:
                raise forms.ValidationError(str(e))
        else:
            user = self.instance.user
            user.username = username
            
        user.first_name = cd.get('first_name')
        user.last_name = cd.get('last_name')  
        user.save()
        
        profile = super(NewScoutForm, self).save(*args, **kwargs)
        profile.user = user
        profile.birthday = self.bd_date
        profile.save()
        return profile
        
            
        