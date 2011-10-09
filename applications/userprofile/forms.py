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
            print u, self.instance.user
            if u != self.instance.user:
            #if u.profile != self.instance:
                raise forms.ValidationError('A user with that login already exists.')
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
        profile.save()
        return profile
        
            
        