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
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import requests

MIN_LENGTH = 8
MAX_FILESIZE = 100*1024 #in bytes
MAX_HEIGHT = 50 #in px
MAX_WIDTH = 50 #in px
MIN_PHONE_NUMBER_LENGTH = 8
MAX_PHONE_NUMBER_LENGTH = 12

def get_validate(address):
    return requests.get(
        "https://api.mailgun.net/v3/address/validate",
        auth=("api", settings.MAILGUN_API_KEY),
        params={"address": address})

class ContactForm(forms.Form):
    """
    Form for the send email page on contact page.
    """
    name_visitor = forms.CharField(required=True)
    email_visitor = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(required=True,widget=forms.Textarea(attrs={'class' : 'form-control'})) #form-control activates bootstrap textarea

class UserForm(forms.ModelForm):

    error_messages = {'password_mismatch': _("The two password fields didn't match."),'email_mismatch': _("The two e-mail fields didn't match."),}
    password1 = forms.CharField(required=True,label=_("Password"),widget=forms.PasswordInput)
    password2 = forms.CharField(required=True,label=_("Password confirmation"),widget=forms.PasswordInput,help_text=_("Enter the same password as before, for verification."))
    email = forms.EmailField(label=_("e-mail"))
    email2 = forms.EmailField(label=_("e-mail opnieuw"))
    birthdate = forms.DateField(required=True, widget=SelectDateWidget(years=range(1914,datetime.now().year)))

    class Meta:
        model = User
        fields = ("first_name","last_name","phone_number","study")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_email2(self):
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(self.error_messages['email_mismatch'],code='email_mismatch',)
        if get_validate(email1) == False:
            raise forms.ValidationError("Not a valid e-mail address.")
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
                if image.size>MAX_FILESIZE: #or w > MAX_WIDTH or h > MAX_HEIGHT
                    raise forms.ValidationError(_("Image dimensions or size too large."))
                if width > MAX_WIDTH or height > MAX_HEIGHT: #thumbnail
                    image = Image.open(image)
                    image.thumbnail((MAX_WIDTH,MAX_HEIGHT),Image.ANTIALIAS)
                    io = StringIO.StringIO()
                    image.save(io, 'JPEG')
                    image = InMemoryUploadedFile(io, None, 'avatar.jpg', 'image/jpeg', io.len, None)
            except IOError: #needed because otherwise you'd get this error when registering without an image input (=with default avatar)
                return image
            return image

class UserEditForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("first_name","last_name","phone_number","study","email") 

    password2 = forms.CharField(label=_("password2"),widget=forms.PasswordInput(attrs={'autofocus': ''}),)

    def clean_email(self):
        mail = self.cleaned_data.get("email")
        if get_validate(mail) == False:
            raise forms.ValidationError("Not a valid e-mail address.")
        return mail

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
            if image.size>MAX_FILESIZE:
                raise forms.ValidationError(_("Image file size too large."))
            if width > MAX_WIDTH or height > MAX_HEIGHT: #thumbnail
                image = Image.open(image)
                image.thumbnail((MAX_WIDTH,MAX_HEIGHT),Image.ANTIALIAS)
                io = StringIO.StringIO()
                image.save(io, 'JPEG')
                image = InMemoryUploadedFile(io, None, 'avatar.jpg', 'image/jpeg', io.len, None)
            return image

class BirthdayEditForm(forms.ModelForm):
    """
    Modelform specifically for already created birthday type Events.
    """
    class Meta:
        model = Event
        fields = ['date_of_event']
        widgets = {'date_of_event': SelectDateWidget(years=range(1914,datetime.now().year))}  
            
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

class AddEventForm(forms.ModelForm):
    """
    Form that lets you add an event, which will be displayed on the calendar.
    """

    def __init__(self, *args, **kwargs):
        super(AddEventForm, self).__init__(*args, **kwargs)
        #set 'em all required, in models most are not required because of birthday events with most fields null
        self.fields['name'].required = True
        self.fields['location'].required = True
        self.fields['start_hour'].required = True
        self.fields['end_hour'].required = True
        self.fields['event_color'].required = True

    class Meta:
        model = Event
        fields = ['name', 'location','date_of_event', 'start_hour','end_hour','event_color', 'absolute_url', 'board']
        widgets = {
        'date_of_event': SelectDateWidget(), 
        'end_hour': forms.TextInput(attrs={'class' : 'form-control'}), #form-control activates bootstrap textarea
        'start_hour': forms.TextInput(attrs={'class': 'form-control'}) #form-control activates bootstrap textarea
        }
        #not yet displayed, for when crispy forms will be used with all these forms
        help_texts = {'event_color':_("1 = repetitie, 2 = concert, 3 = activiteit, 5 = repetitieweekend")}

    def clean_event_color(self):
        color = self.cleaned_data['event_color']
        if not color == "1" and not color == "2" and not color == "3" and not color == "4" and not color == "5" and not color == "42":
            raise forms.ValidationError('Invalid number "{}".'.format(color))
        elif color == "42":
            raise forms.ValidationError("The meaning of life isn't a color code.")
        return color



