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

    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)

    #     self.fields['password'].required = False
    #     self.fields['confirmpassword'].required = False
    
    error_css_class = 'error' 
    confirmpassword = CharField('confirmpassword', max_length=50, blank=False)

    def saveTotal(self, commit=True): #overwrite needed to store password correctly
        user = super(UserForm, self).save(commit=False)
        user.set_password(user.password) # set password properly before commit
        if commit:
            user.save()
        return user
    def clean_confirmpassword(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirmpassword2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2



class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['groups']
        exclude = ['associated_user'] #excluded and added later
    
    error_css_class = 'error'
