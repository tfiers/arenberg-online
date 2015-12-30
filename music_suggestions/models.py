from django.db.models import (
	Model, CharField, URLField, TextField, ForeignKey
)
from core.models import User

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