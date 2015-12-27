import datetime
from django.db import models
from django.core.mail import send_mail
from django.db.models import (
    EmailField, CharField, BooleanField, DateTimeField, TimeField,DateField, Model,
    OneToOneField, IntegerField, ManyToManyField, ForeignKey )
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager )
import os
from django.conf import settings
import datetime

class Document(models.Model):
    docfile = models.FileField(upload_to='uploads/')


class UserManager(BaseUserManager):
    """
    Manager for the User model defined below.

    Adapted from the Django source code 'UserManager' to use the email address as 
    the identifier instead of a custom username.

    Source: https://github.com/django/django/blob/master/django/contrib/auth/models.py#L166
    """
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email),
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured user model with admin-compliant permissions.
    Email and password are required. Other fields are optional.

    Adapted from the Django source code 'User' to use the email address as 
    the identifier instead of a custom username.

    Source: https://github.com/django/django/blob/master/django/contrib/auth/models.py#L379
    """
    email = EmailField(_('email address'), max_length=255, unique=True,
        error_messages={
            'unique': _("A user with that email adress already exists."),
        })
    first_name = CharField(_('first name'), max_length=50, blank=False)
    last_name = CharField(_('last name'), max_length=50, blank=False)
    phone_number = CharField(_('phone_number'), max_length=15, blank=False) 
    study = CharField(_('study'), max_length=50, blank=False) 
    is_staff = BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_board = BooleanField(_('board'), default=False,
        help_text=_('Designates whether the user is part of the board and can view board content.'))
    is_active = BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    approved = BooleanField(_('approved'), default=False,
        help_text=_('Designates whether this user is approved and may view the login only content.'))
    date_joined = DateTimeField(_('date joined'), default=timezone.now)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    # From the docs:
    # "REQUIRED_FIELDS: A list of the field names that will be prompted for 
    # when creating a user via the createsuperuser management command. [..]
    # REQUIRED_FIELDS has no effect in other parts of Django, like creating 
    # a user in the admin. [..] REQUIRED_FIELDS must contain all required fields 
    # on your User model, but should not contain the USERNAME_FIELD or password 
    # as these fields will always be prompted for.
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the user's first name.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __unicode__(self):
        name = self.get_full_name()
        if name:
            return name
        else:
            return u"[{}]".format(self.email)

    class Meta:
        ordering = ['first_name']


class UserProfile(Model):
    associated_user = OneToOneField(User, null=True, default=None)
    old_drupal_uid = IntegerField(blank=True, null=True, default=None)
    last_password_change = DateTimeField(blank=True, null=True, default=None)
    groups = ManyToManyField('Group', blank=False)
    avatar = models.ImageField(upload_to='images/avatars',default='media/defaultavatar.png')
    
    def __unicode__(self):
        return u"User profile for {}".format(self.associated_user)

    @property   
    def groups_as_string(self):
        return ", ".join([str(g) for g in self.groups.all()])


class Group(Model):
    ''' A 'Group' (or a 'Role' if there is only one User in it) is 
        a collection of Users, for sending emails or showing specific
        content to. '''

    STANDARD, MUSICAL, PROJECT = 'standard', 'musical', 'project'
    category_choices = (
        (STANDARD, _('Standaard')), # ouwzakken, bestuur, techniek, ...
        (MUSICAL, _('Muzikaal')), # trompetten, strijkers.snowman, pv.violen1, ...
        (PROJECT, _('Project')), # full-orchestra, snowman, china, ...
    )

    name = CharField(max_length=150)
    category = CharField(max_length=14, choices=category_choices, default=STANDARD)
    children = ManyToManyField('self', symmetrical=False, related_name='parents', 
        blank=True)
    email_address = CharField(max_length=100, blank=True,
        help_text="If different from a sanitized version of 'name'")

    def __unicode__(self):
        return u"{} ({})".format(self.name, self.category)

    @property   
    def parents_as_string(self):
        return ", ".join([str(p) for p in self.parents.all()])

    def get_all_descendant_groups(self, include_self=True):
        results = []
        if include_self:
            results.append(self)
        for g in Group.objects.filter(parents=self):
            results.extend(g.get_all_descendant_groups(include_self=True))
        return results

class AlternativeGroupName(Model):
    name = CharField(max_length=150)
    group = ForeignKey(Group)
    email_address = CharField(max_length=100, blank=True, 
        help_text="If different from a sanitized version of 'name'")

    def __unicode__(self):
        return u"Alternative name '{}' for {}".format(self.name, self.group)

class Event(Model):
    name = CharField(max_length=50)
    location  = CharField(max_length=50,null=True,blank=True)
    start_hour = TimeField(null=True, blank=True)
    end_hour = TimeField(null=True, blank=True)
    event_color = CharField(max_length=1,default="1",help_text=_("Color code on calendar. Default (1) is red (rehearsal). 2 = concert, 3 = organised event, 4 = birthday, 5 = repetitieweekend."))
    date_of_event = DateField(max_length=50) 
    board = BooleanField(default=False,help_text=_('Designates whether the event is for is_board users only.'))
    absolute_url = CharField(max_length=100,null=True,blank=True,help_text=_("It's possible to make the event link to a page (opened in a tab)."))
    birthday_user = OneToOneField(User,null=True,blank=True,help_text=_("If this event is a birthday, this attr holds the user."))

    def __unicode__(self):
        return u"'{}', {}".format(self.name, self.date_of_event)
