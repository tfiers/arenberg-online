from django import forms
from models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User 
        fields = ['first_name','last_name','email','password']
    
    error_css_class = 'error'
    #required_css_class = 'required'    

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
        exclude = ['associated_user']
    
    error_css_class = 'error'
    #required_css_class = 'required'

    def saveTotal(self, commit=True): #overwrite needed to store password correctly
        user = super(UserProfileForm, self).save(commit=False)
        user.groups = request.POST.get('groups')  # set groups properly before commit
        if commit:
            user.save()
        return user
    