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
	exclude = ['is_staff','is_active','date_joined','user_permissions','last_login','is_superuser','groups']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user','old_drupal_uid','associated_user','last_password_change']
    
