from django.db.models import (
	Model, CharField, TextField, BooleanField
)

def bool_to_yes_no(boolean):
	return "Yes" if boolean == True else "No"

class NewSemesterAnswer(Model):
	name = CharField(max_length=200)
	plans = TextField(blank=True)
	next_semester = BooleanField(default=False)
	engage = BooleanField(default=False)

	def __unicode__(self):
		return u"Answer by {} - Playing next semester: {}".format(
			self.name, bool_to_yes_no(self.next_semester))
