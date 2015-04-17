from django.core.management.base import BaseCommand
from ticketing.models import Production, Performance, PriceCategory
from datetime import datetime
import django.utils.timezone as django_tz

help_string = ('Creates the necessary Production, Performance, and PriceCategory '
			   'objects to start ticketing for the 2015 S P A C E concerts, if they '
			   'do not exist yet.')
def setup_space_ticketing():
	tz = django_tz.get_default_timezone()
	# update_or_create() returns a tuple: (object, created), that's why we retain
	# only the first element with [0]
	vvk_cc = PriceCategory.objects.update_or_create(
		name="Cultuurkaart in VVK (vanaf winter 2014)", price=4)[0]
	vvk_stud = PriceCategory.objects.update_or_create(
		name="Student in VVK (vanaf winter 2014)", price=5)[0]
	vvk_non_stud = PriceCategory.objects.update_or_create(
		name="Niet-student in VVK (vanaf winter 2014)", price=9)[0]
	vvk_zaventem = PriceCategory.objects.update_or_create(
		name="Zaventem VVK SPACE", price=10)[0]

	space = Production.objects.update_or_create(
		name="S P A C E - Lente 2015")[0]

	do = Performance.objects.get_or_create(
		production=space, location="PDS", 
		date=datetime(2015, 5, 7, 20, 30, tzinfo=tz))[0]
	do.price_categories = [vvk_cc, vvk_stud, vvk_non_stud]
	do.save()

	vr = Performance.objects.get_or_create(
		production=space, location="PDS", 
		date=datetime(2015, 5, 8, 20, 30, tzinfo=tz))[0]
	vr.price_categories = [vvk_cc, vvk_stud, vvk_non_stud]
	vr.save()

	za = Performance.objects.get_or_create(
	  production=space, location="Zaventem", 
	  date=datetime(2015, 5, 9, 20, 00, tzinfo=tz))[0]
	za.price_categories = [vvk_zaventem]
	za.save()


class Command(BaseCommand):
	args = 'none'
	help = help_string

	def handle(self, *args, **options):
		setup_space_ticketing()
		self.stdout.write('Succesfully set-up S P A C E ticketing.')