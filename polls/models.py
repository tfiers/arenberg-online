from django.utils.translation import ugettext_lazy as _
from django.db.models import (
	Model, CharField, URLField, TextField, BooleanField, DateTimeField, ForeignKey, OneToOneField )
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

class NewSemester(Model):
	user = OneToOneField(User,null=True) #user is added automatically in views, so it isn't a big problem, but this is a quick dirty fix: null should be False
	#DO NOT CONVERT BACK, CHANGING NULL=TRUE TO NULL=FALSE MIGHT BREAK DATABASE/MIGRATIONS IN DJANGO 1.7.1
	plans = TextField(blank=True)
	next_semester = BooleanField(default=False)
	engage = BooleanField(default=False)

	def __unicode__(self):
		if self.user==None: #protection because null=True on user field
			return u"Playing next semester: {}".format("Yes" if self.next_semester else "No")
		return u"Answer by {} - Playing next semester: {}".format(self.user, "Yes" if self.next_semester else "No")

class PieceOfMusic(Model):
	title = CharField(max_length=200, unique=True)
	link_to_recording = URLField(unique=True, blank=True)
	sheet_music = TextField(null=True,blank=True)
	suggested_by = ForeignKey(User, blank=True, null=True)
	suggested_by_string = CharField(max_length=200, blank=True)

	class Meta:
		ordering = ['-id']
		verbose_name_plural = "pieces of music"

	def __unicode__(self):
		return u"'{}' (suggested by {})".format(
			self.title, self.suggested_by_string)

class Feature(Model):
	name = CharField(max_length=500, unique=True)
	description = TextField(null=True,blank=True)
	suggested_by = ForeignKey(User, blank=True, null=True)
	#suggested_by_string = CharField(max_length=200, blank=True) #user who suggested feature will not be displayed so it's not a needed field

	class Meta:
		ordering = ['-id']
		verbose_name_plural = "features"

	def __unicode__(self):
		return u"'{}'".format(self.name)

class Vote(Model):
	"""
	Used to let approved users vote on suggested pieces of music.
	"""
	receiving_piece = ForeignKey(PieceOfMusic)
	voter = ForeignKey(User)

	def __unicode__(self):
		return u"Vote from {} for {}".format(
			self.voter, self.receiving_piece)
		