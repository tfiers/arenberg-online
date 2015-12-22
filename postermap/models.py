from django.db.models import ( Model, FloatField, ForeignKey, 
	PositiveSmallIntegerField, CharField, DateTimeField,
	ManyToManyField, TextField )
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import User
from ticketing.models import Production
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Poster(Model):
	latitude = FloatField()
	longitude = FloatField()
	hanging_date = DateTimeField()
	for_what = GenericForeignKey('for_what_type', 'for_what_id')
	for_what_type = ForeignKey(ContentType)
	for_what_id = PositiveSmallIntegerField()
	production = ForeignKey(Production,null=True) #production is added in view, so it's more or less OK, but null should be False (was a quick and dirty fix for migrations)
	#DO NOT CONVERT BACK, CHANGING NULL=TRUE TO NULL=FALSE MIGHT BREAK DATABASE/MIGRATIONS IN DJANGO 1.7.1
	location_name = CharField(max_length=400, blank=True)
	count = PositiveSmallIntegerField(default=1)
	hung_by = ManyToManyField(User, blank=True, related_name='hung_posters')
	entered_by = ForeignKey(User, null=True, blank=True, related_name='entered_posters')
	entered_on = DateTimeField(null=True, blank=True)
	remarks = TextField(blank=True)
	BRUSH_AND_GLUE, PUSHPIN, TAPE, OTHER = 'brush_and_glue', 'pushpin', 'tape', 'other'
	attachment_type_choices = (
		(BRUSH_AND_GLUE, _('Borstel en lijm')),
		(PUSHPIN, _('Punaises')),
		(TAPE, _('Plakband')),
		(OTHER, _('Anders')),
	)
	attachment_type = CharField(
		max_length=14, choices=attachment_type_choices, null=True, blank=True)

	def __unicode__(self):
		if self.count > 1:
			return u"{} posters bij {} door {}".format(
				self.count, self.location_name, self.authors_as_string)
		else:
			return u"Poster bij {} door {}".format(
				self.location_name, self.authors_as_string)

	@property
	def authors_as_string(self):
		authors = [str(self.entered_by)]
		authors.extend([str(accomplice) for accomplice in list(self.hung_by.all())])
		return ", ".join(authors)

	@property
	def authors(self):
		authors = [self.entered_by]
		authors.extend([accomplice for accomplice in list(self.hung_by.all())])
		return authors