import django_tables2 as tables
from models import User, Event, UserProfile
from django.utils.translation import ugettext_lazy as _

class UserTable(tables.Table):
    class Meta:
        model = User
        attrs = {"class": "paleblue"} # <table> class
        fields = ('first_name', 'last_name','date_of_birth','study','email','phone_number','groups',)
    date_of_birth = tables.Column(accessor = 'event.date_of_event',verbose_name=_('Geboortedatum'))
    groups = tables.Column(order_by='groups',accessor = 'userprofile.groups_as_string',verbose_name=_('Groepen'))