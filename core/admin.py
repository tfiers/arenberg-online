from core.models import User, UserProfile, Group, AlternativeGroupName
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
import django.contrib.auth.admin

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email address and
    password.

    Adapted from: https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L71
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("email",)

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
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Adapted from: https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L107
    """
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(django.contrib.auth.admin.UserAdmin):
    """
    See superclass source code:
    https://github.com/django/django/blob/master/django/contrib/auth/admin.py#L40
    """
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','birthdate','study','phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_board', 'is_superuser', 'approved',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'birthdate','study', 'phone_number', 'is_staff', 'is_board','approved', 'date_joined', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    change_form_template = 'loginas/change_form.html'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('associated_user', 'old_drupal_uid', 'last_password_change', 'groups_as_string')
    ordering = ('last_password_change',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'parents_as_string')


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(AlternativeGroupName)
