from django.utils.translation import ugettext_lazy as _
from django.db.models import (
	Model, CharField, TextField, BooleanField, DateTimeField, ForeignKey, OneToOneField )
from core.models import User
from datetime import datetime
from pytz import utc

class PollAnswer(Model):
	date_submitted = DateTimeField(null=True, blank=True)
	# Automatically set the date_submitted when an object is
	# save to the database.
	def save(self, *args, **kwargs):
		if not self.id: # This object is not already in the database.
			self.date_submitted = datetime.now(utc)
		super(PollAnswer, self).save(*args, **kwargs)

class NewSemester(Model):
	# user = OneToOneField(User)
	plans = TextField(blank=True)
	next_semester = BooleanField(default=False)
	engage = BooleanField(default=False)

	def __unicode__(self):
		return u"Answer by {} - Playing next semester: {}".format(
			self.name, "Yes" if self.next_semester else "No")

class ZaventemTransport(PollAnswer):
	musician = ForeignKey(User)
	GROUP, OWN = 'group', 'own'
	transport_choices = (
		(GROUP, _('.. met de groep')),
		(OWN, _('.. met eigen vervoer')))
	transport = CharField(
		max_length=5, choices=transport_choices, default=GROUP)

	def __unicode__(self):
		return u"Answer by {} - Goes to Zaventem: {}".format(
			self.musician, self.transport)
		