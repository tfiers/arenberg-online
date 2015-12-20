from django import forms
from django.contrib.auth.models import check_password
from models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )

class UserForm(forms.ModelForm):

    confirmpassword = forms.CharField(widget=forms.PasswordInput(),required=True)
    confirmemail = forms.EmailField(required=True)
    
    class Meta:
        model = User 
        fields = ['first_name','last_name','email','password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    error_css_class = 'error' 



    def saveTotal(self, commit=True): #overwrite needed to store password correctly
        user = super(UserForm, self).save(commit=False)
        user.set_password(user.password) # set password properly before commit
        if commit:
            user.save()
        return user
    
    def clean_password(self):
        #assert self.data["password"] != None
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirmpassword'):
            raise forms.ValidationError('The passwords are not the same.')
        return self.cleaned_data.get('password')

    def clean_email(self):
        if self.cleaned_data.get('email') != self.cleaned_data.get('confirmemail'):
            raise forms.ValidationError('The e-mail addresses are not the same.')
        return self.cleaned_data.get('email')
    
    def clean(self,*args, **kwargs):
        self.clean_password()
        self.clean_email()
        return super(UserForm, self).clean(*args, **kwargs)



class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['groups']
        exclude = ['associated_user'] #excluded and added later in views.py
    
    error_css_class = 'error'
