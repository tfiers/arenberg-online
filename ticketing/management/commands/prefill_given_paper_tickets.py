from django.core.management.base import BaseCommand
from given_paper_tickets import given_paper_tickets
from core.models import User
from ticketing.models import GivenPaperTickets, Performance
from datetime import datetime, date
from django.contrib.contenttypes.models import ContentType
import django.utils.timezone as django_tz

def fill_in_existing_data():
	do = Performance.objects.get(date__contains=date(2015,5,7))
	vr = Performance.objects.get(date__contains=date(2015,5,8))

	tz = django_tz.get_default_timezone()

	for tup in given_paper_tickets['23 for do']:
		GivenPaperTickets.objects.update_or_create(
			given_on=datetime(2015,4,23,22,45,tzinfo=tz),
			given_to=User.objects.get(first_name__iexact=tup[0], last_name__iexact=tup[1]),
			for_what_type=ContentType.objects.get_for_model(Performance),
			for_what_id=do.id,
			count=tup[2],
		)

	for tup in given_paper_tickets['23 for vr']:
		GivenPaperTickets.objects.update_or_create(
			given_on=datetime(2015,4,23,22,45,tzinfo=tz),
			given_to=User.objects.get(first_name__iexact=tup[0], last_name__iexact=tup[1]),
			for_what_type=ContentType.objects.get_for_model(Performance),
			for_what_id=vr.id,
			count=tup[2],
		)

	for tup in given_paper_tickets['30 for do']:
		GivenPaperTickets.objects.update_or_create(
			given_on=datetime(2015,4,30,22,45,tzinfo=tz),
			given_to=User.objects.get(first_name__iexact=tup[0], last_name__iexact=tup[1]),
			for_what_type=ContentType.objects.get_for_model(Performance),
			for_what_id=do.id,
			count=tup[2],
		)

	for tup in given_paper_tickets['30 for vr']:
		GivenPaperTickets.objects.update_or_create(
			given_on=datetime(2015,4,30,22,45,tzinfo=tz),
			given_to=User.objects.get(first_name__iexact=tup[0], last_name__iexact=tup[1]),
			for_what_type=ContentType.objects.get_for_model(Performance),
			for_what_id=vr.id,
			count=tup[2],
		)



class Command(BaseCommand):
	args = 'none'
	help = "yo do this"

	def handle(self, *args, **options):
		fill_in_existing_data()
		self.stdout.write('Succesfully filled in existing given_paper_tickets data.')