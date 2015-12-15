from django import forms
from django.contrib.auth.models import check_password
from models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.template import RequestContext

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User 
        fields = ['first_name','last_name','email','password']
    
    error_css_class = 'error' 

    def saveTotal(self, commit=True): #overwrite needed to store password correctly
        user = super(UserForm, self).save(commit=False)
        user.set_password(user.password) # set password properly before commit
        if commit:
            user.save()
        return user



class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['groups']
        exclude = ['associated_user'] #excluded and added later
    
    error_css_class = 'error'

class UserFormUpdate(forms.ModelForm):
    
    class Meta:
        model = User 
        fields = ['first_name','last_name','email','password']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserFormUpdate, self).__init__(*args, **kwargs)
    
    error_css_class = 'error' 
    old_password = CharField(max_length=50)

    def saveTotal(self, commit=True): #overwrite needed to store password correctly
        user = super(UserForm, self).save(commit=False)
        user.set_password(user.password) # set password properly before commit
        if commit:
            user.save()
        return user

    def clean(self): #for password confirmation on edit, this function is used by is_valid so error will be passed and shown on
        password = self.cleaned_data.get('old_password')
        if not self.user.check_password(password):
            raise forms.ValidationError("Wrong password")

        return self.cleaned_data



class UserProfileFormUpdate(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['groups']
        exclude = ['associated_user'] #excluded and added later
    
    error_css_class = 'error'


    
