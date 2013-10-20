import hashlib
from django import forms
from unit.models import Unit, UnitRequest

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ('council','calendar')

    user_role = forms.IntegerField()
    council_name = forms.CharField(max_length=255)
    
class UnitRequestForm(forms.ModelForm):
    class Meta:
        model = UnitRequest
    
        
    def __init__(self, *args, **kwargs):
        scout = kwargs.pop("scout", None)
        super(UnitRequestForm, self).__init__(*args, **kwargs)
        type = self.initial.get("type", 'request')
        
        if scout and type == 'request':
            
            self.initial = {"email":scout.email,"member":scout.profile, 'type':'request'}   
            self.fields['email'].widget = forms.widgets.HiddenInput()
            self.fields['type'].widget = forms.widgets.HiddenInput()
            self.fields['member'].widget = forms.widgets.HiddenInput()
            self.fields['key'].widget = forms.widgets.HiddenInput()
            
        elif type == 'invite':
            m = hashlib.sha1()
            key = "%s-%s"%(self.initial['email'], self.initial['member'].email)
            print key
            m.update("%s-%s"%(self.initial['email'], self.initial['member'].email))
            key = m.hexdigest()
            self.initial['key'] = key
            
            print 'initial',self.initial
            
    def clean(self, *args, **kwargs):
        print 'clean data', self.cleaned_data
        
        return self.cleaned_data