from django import forms
from django.contrib.auth.models import check_password
from django.contrib.auth.models import User
from models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from core.models import Group
from django.contrib.admin import widgets


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )

class UserForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'email_mismatch': _("The two e-mail fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."))
    email = forms.EmailField(label=_("e-mail"))
    email2 = forms.EmailField(label=_("e-mail opnieuw"))

    class Meta:
        model = User
        fields = ("first_name","last_name")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_email2(self):
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )

        return email2

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['groups']
        exclude = ['associated_user'] #excluded and added later in views.py
    
    error_css_class = 'error'

class UserEdit(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserEdit, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("first_name","last_name","email")    

    password2 = forms.CharField(
        label=_("password2"),
        widget=forms.PasswordInput(attrs={'autofocus': ''}),
    )

    def clean_password2(self):
        """
        Validates that the password2 field is correct.
        """
        password2 = self.cleaned_data["password2"]
        if not self.user.check_password(password2):
            raise forms.ValidationError(_("Your password was entered incorrectly. Please enter it again."))
        return password2


class UserProfileEdit(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['groups']
        exclude = ['associated_user'] #excluded and added later in views.py
        widgets={'groups': forms.CheckboxSelectMultiple}

    def __init__(self, user, *args, **kwargs):
        self.user=user
        super(UserProfileEdit, self).__init__(*args, **kwargs)

    #groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=widgets.FilteredSelectMultiple("verbose name", is_stacked=False))
    
    error_css_class = 'error'
