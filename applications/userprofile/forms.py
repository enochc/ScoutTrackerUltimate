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
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=False)
    email = forms.CharField(max_length=50, required=False)
    bd_string = forms.CharField(max_length=50, required=False)
    
    bd_date = None
    
    def clean_bd_string(self):
        bd_string = self.cleaned_data['bd_string']
        if len(bd_string) > 0:
            bd = datetime.datetime.strptime(bd_string, '%b %d, %Y')
            self.bd_date = bd
            return bd_string   
        else:
            return None 
    
    def clean_login_name(self):
        username = self.cleaned_data['login_name']
        troop = self.cleaned_data['troop']
        gid = self.cleaned_data['google_id']
        if len(gid) > 0:
            username='g:%s' %  gid
        else:
            username='%s_%s' % (username, troop or '100000')
        try:
            u = User.objects.get(username__iexact=username)
            if u != self.instance.user:
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
                password = cd.get('password','password')
                user = User.objects.create_user(username, '', password=password)
            except Exception, e:
                raise forms.ValidationError(str(e))
        else:
            user = self.instance.user
            user.username = username
            
        user.first_name = cd.get('first_name')
        user.last_name = cd.get('last_name') 
        user.email = cd.get('email') 
        
        
        profile = super(NewScoutForm, self).save(*args, **kwargs)
        if len(profile.google_id) > 0:
            user.is_active = False
        profile.user = user
        profile.birthday = self.bd_date
        
        user.save()
        profile.save()
        return profile
        
            
        