import datetime

from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import date as _date

from userprofile.models import Userprofile

class NewScoutForm(forms.ModelForm):

        
    class Meta:
        model = Userprofile
        exclude = ('user','goals','awards')
    
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    login_name = forms.CharField(max_length=50, required=False)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(), required=False)
    email = forms.CharField(max_length=50)
    bd_string = forms.CharField(max_length=50, required=False)
    
    
    def __init__(self, *args, **kwargs):
        
        super(NewScoutForm, self).__init__(*args, **kwargs)
        if self.instance:
            unit = self.instance.unit
        else:
            unit = self.initial.get("unit")

        if unit:
            self.fields['patrol']=forms.ModelChoiceField(queryset=unit.patrol_set.all())
        
    
    bd_date = None
    
    def clean_bd_string(self):
        bd_string = self.data['bd_string']
        if len(bd_string) > 0:
            try:
                bd = datetime.datetime.strptime(bd_string, '%b %d, %Y')
            except:
                try:
                    bd = datetime.datetime.strptime(bd_string, '%Y-%m-%d')
                except:
                    return None
            self.bd_date = bd
            return bd_string   
        else:
            return None 
        
    def clean_email(self):
        email = self.cleaned_data['email']
        print 'clean email', email
        if email != 'noemail':
            try:
                user = User.objects.get(email__iexact=email)
                if not self.instance or user != self.instance.user:
                    print self.instance.user, user
                    raise forms.ValidationError('A user with that email already exists.')
            except User.DoesNotExist:
                return email
        else:
            return email
    
    def clean_login_name(self):
        username = self.data['email']
        if username =='noemail':
            return "%s_%s_%s"%(self.data.get("first_name"),self.data.get("last_name"),self.data.get("unit"))
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
        
            
        