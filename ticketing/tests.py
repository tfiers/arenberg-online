# coding: utf-8

from django.test import TestCase
from ticketing.management.commands.setup_space_ticketing import setup_space_ticketing
from ticketing.models import (
	Production, Performance, PriceCategory, Order, Performance, Ticket )
from datetime import date, datetime
import django.utils.timezone as django_tz
import pytz

a_certain_time = datetime.now(pytz.utc)

def create_order():
	space_vr = Performance.objects.get(date__contains=date(2015,5,8))
	return Order.objects.create(
			performance=space_vr,
			first_name="Henk",
			last_name="Douwe",
			email="henk@bakkerij-henk.com",
			payment_method="cash",
			date=a_certain_time
		)
	

class SpaceTicketingTest(TestCase):

	@classmethod
	def setUpClass(self):
		setup_space_ticketing()

	def test_space_ticketing_setup(self):
		space = Production.objects.filter(name__contains="S P A C E")[0]
		self.assertEqual(str(space), "S P A C E - Lente 2015")

		do = Performance.objects.get(date__contains=date(2015,5,7))
		vr = Performance.objects.get(date__contains=date(2015,5,8))
		za = Performance.objects.get(date__contains=date(2015,5,9))
		self.assertEqual(do.production, space)
		self.assertEqual(vr.production, space)
		self.assertEqual(za.production, space)
		self.assertEqual(do.location, "PDS")
		self.assertEqual(vr.location, "PDS")
		self.assertEqual(za.location, "Zaventem")

		self.assertEqual(vr.date.minute, 30)
		
		self.assertEqual(str(do),
			'"S P A C E - Lente 2015" on Thu May 07 20:30 @ PDS')
		self.assertEqual(str(vr),
			'"S P A C E - Lente 2015" on Fri May 08 20:30 @ PDS')
		self.assertEqual(str(za),
			'"S P A C E - Lente 2015" on Sat May 09 20:00 @ Zaventem')


		vvk_cc = PriceCategory.objects.get(
			full_name="Cultuurkaart in VVK (vanaf winter 2014)", price=4)
		vvk_stud = PriceCategory.objects.get(
			full_name="Student VVK (vanaf winter 2014)", price=5)
		vvk_non_stud = PriceCategory.objects.get(
			full_name="Niet-student in VVK (vanaf winter 2014)", price=9)
		vvk_zaventem = PriceCategory.objects.get(
			full_name="Zaventem VVK SPACE", price=10)
		self.assertEqual(str(vvk_stud), '"Student VVK (vanaf winter 2014)": € 5')


	def test_create_order(self):
		self.assertEqual(len(Order.objects.all()), 0)
		order = create_order()
		self.assertEqual(len(Order.objects.all()), 1)
		self.assertEqual(Order.objects.all()[0], order)

	def test_get_order(self):
		order = create_order()
		self.assertEqual(Order.objects.get(last_name="Douwe"), order)

	def test_remarks(self):
		order = create_order()
		self.assertEqual(order.user_remarks, None)
		order.user_remarks = "Waar kan ik mijn kruiwagen parkeren?"
		order.save()
		self.assertEqual(order.user_remarks, "Waar kan ik mijn kruiwagen parkeren?")

		self.assertEqual(order.admin_remarks, None)
		order.admin_remarks = "Deze man is een fenomeen."
		order.save()
		self.assertEqual(order.admin_remarks, "Deze man is een fenomeen.")

	def test_delete_order(self):
		order = create_order()
		self.assertEqual(len(Order.objects.all()), 1)
		self.assertEqual(Order.objects.all()[0], order)
		order.delete()
		self.assertEqual(len(Order.objects.all()), 0)

	def test_order_string_representation(self):
		order = create_order()
		self.assertEqual(str(order), "Online order by Henk Douwe on {}.".format(
			a_certain_time.strftime('%d-%m-%Y %H:%M:%S')))

	def test_datetime_formatting(self):
		tz = django_tz.get_default_timezone()
		self.assertEqual("Fri May 08 20:30", "{:%a %b %d %H:%M}".format(
			datetime(2015, 5, 8, 20, 30, tzinfo=tz)))

	def test_performance_datetime(self):
		tz = django_tz.get_default_timezone()
		vr = Performance.objects.get(date__contains=date(2015,5,8))
		self.assertEqual(vr.date, datetime(2015, 5, 8, 20, 30, tzinfo=tz))

	def test_sum_ticket_prices(self):
		order = create_order()
		vvk_cc = PriceCategory.objects.get(
			name="Cultuurkaart in VVK (vanaf winter 2014)", price=4)
		vvk_stud = PriceCategory.objects.get(
			name="Student VVK (vanaf winter 2014)", price=5)
		vvk_non_stud = PriceCategory.objects.get(
			name="Niet-student in VVK (vanaf winter 2014)", price=9)
		vvk_zaventem = PriceCategory.objects.get(
			name="Zaventem VVK SPACE", price=10)

		ticket_1 = Ticket.objects.create(order=order, price_category=vvk_cc)
		ticket_2 = Ticket.objects.create(order=order, price_category=vvk_stud)
		ticket_3 = Ticket.objects.create(order=order, price_category=vvk_stud)
		ticket_4 = Ticket.objects.create(order=order, price_category=vvk_non_stud)

		self.assertEqual(order.total_price(), 23)

		space_za = Performance.objects.get(date__contains=date(2015,5,9))