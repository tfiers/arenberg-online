from django import forms
from django.contrib.auth.models import check_password
from django.contrib.auth.models import User
from models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from core.models import Group
from datetime import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.core.files.images import get_image_dimensions
from PIL import Image

MIN_LENGTH = 8
MAX_FILESIZE = 20*1024 #in bytes
MAX_HEIGHT = 50 #in px
MAX_WIDTH = 50 #in px
MIN_PHONE_NUMBER_LENGTH = 9
MAX_PHONE_NUMBER_LENGTH = 10

class UserForm(forms.ModelForm):

    error_messages = {'password_mismatch': _("The two password fields didn't match."),'email_mismatch': _("The two e-mail fields didn't match."),}
    password1 = forms.CharField(label=_("Password"),widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),widget=forms.PasswordInput,help_text=_("Enter the same password as before, for verification."))
    email = forms.EmailField(label=_("e-mail"))
    email2 = forms.EmailField(label=_("e-mail opnieuw"))

    class Meta:
        model = User
        fields = ("first_name","last_name","phone_number","study","birthdate")
        widgets = {'birthdate': SelectDateWidget(years=range(1914,datetime.now().year))}

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_email2(self):
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(self.error_messages['email_mismatch'],code='email_mismatch',)
        return email2

    def clean_phone_number(self):
        pn = self.cleaned_data.get("phone_number")
        if (not len(pn) in range(MIN_PHONE_NUMBER_LENGTH,MAX_PHONE_NUMBER_LENGTH+1)) and not pn.isdigit():
            raise forms.ValidationError(_("Invalid phone number."))
        return pn

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1)<MIN_LENGTH:
            raise forms.ValidationError(_("The password must be at least 8 characters long."))
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'],code='password_mismatch',)
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.birthdate = self.cleaned_data['birthdate']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['groups','avatar']
        exclude = ['associated_user'] #excluded and added later in views.py
        widgets = {'groups': forms.CheckboxSelectMultiple()}
    
    error_css_class = 'error'

    def clean_avatar(self):
        image = self.cleaned_data.get('avatar',False)
        if image:
            try:
                width, height = get_image_dimensions(image)
                if width > MAX_WIDTH or height > MAX_HEIGHT or image.size>MAX_FILESIZE: #or w > MAX_WIDTH or h > MAX_HEIGHT
                    raise forms.ValidationError(_("Image dimensions or size too large."))
            except IOError: #needed because otherwise you'd get this error when registering without an image input (=with default avatar)
                return image
            return image

class UserEditForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("first_name","last_name","phone_number","study","email","birthdate")  
        widgets = {'birthdate': SelectDateWidget(years=range(1914,datetime.now().year))}  

    password2 = forms.CharField(label=_("password2"),widget=forms.PasswordInput(attrs={'autofocus': ''}),)

    def clean_phone_number(self):
        pn = self.cleaned_data.get("phone_number")
        if (not len(pn) in range(MIN_PHONE_NUMBER_LENGTH,MAX_PHONE_NUMBER_LENGTH+1)) and not pn.isdigit():
            raise forms.ValidationError(_("Invalid phone number."))
        return pn

    def clean_password2(self):
        """
        Validates that the password2 field is correct.
        """
        password2 = self.cleaned_data["password2"]
        if not self.user.check_password(password2):
            raise forms.ValidationError(_("Your password was entered incorrectly. Please enter it again."))
        return password2


class UserProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['groups','avatar']
        exclude = ['associated_user'] #excluded and added later in views.py
        widgets = {'groups': forms.CheckboxSelectMultiple()}
    
    error_css_class = 'error'

    def clean_avatar(self):
        image = self.cleaned_data.get('avatar',False)
        if image:
            width, height = get_image_dimensions(image)
            if width > MAX_WIDTH or height > MAX_HEIGHT or image.size>MAX_FILESIZE: #or w > MAX_WIDTH or h > MAX_HEIGHT
                raise forms.ValidationError(_("Image dimensions or size too large."))
            return image
            
class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two new password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        #password check
        if len(password1)<MIN_LENGTH:
            raise forms.ValidationError("The password must be at least 8 characters long.")
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(self.error_messages['password_mismatch'],code='password_mismatch',)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class CustomPasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput(attrs={'autofocus': ''}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


