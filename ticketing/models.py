# coding: utf-8

from django.utils.translation import ugettext_lazy as _
from django.db.models import (
	Model, ForeignKey, CharField, DateField, TimeField, FloatField, 
	EmailField, DateTimeField, TextField, PositiveSmallIntegerField
)

class Production(Model):
	"""
	A production (a concert series) identified by a name and being performed 
	at one or more occasions ('Performances').
	"""
	name = CharField(max_length=200, unique=True)

	def __unicode__(self):
		return self.name


class Performance(Model):
	"""
	A performance of a production on a certain date and location.
	"""
	production = ForeignKey(Production)
	date = DateField(blank=True, null=True)
	starting_time = TimeField(blank=True, null=True)
	location = CharField(max_length=200, blank=True)

	def __unicode__(self):
		return u'"{}" on {} @ {}'.format(
			self.production.name, self.date, self.location)


class PriceCategory(Model):
	"""
	A named price class for tickets.
	For example: "Students with a culture card (pre sale)", € 4
	"""
	name = CharField(max_length=200, unique=True)
	price = FloatField()

	def __unicode__(self):
		return u'"{}": € {}'.format(self.name, self.price)

	class Meta:
		verbose_name_plural = "price categories"


class Order(Model):
	"""
	Created when someone orders tickets online.
	"""
	first_name = CharField(max_length=75, blank=True)
	last_name = CharField(max_length=75, blank=True)
	email = EmailField()
	date = DateTimeField(_("date of order"))
	remarks = TextField(_(
		"remarks. For questions, special requests, "
		"answers to 'how did you hear about this?', ..."), blank=True)

	TRANSFER, CASH = 'transfer', 'cash'
	payment_method_choices = (
		# (TRANSFER, _('Bank transfer')), (CASH, _('Cash on the spot'))
		# TODO: translate
		(TRANSFER, _('Via overschrijving')), (CASH, _('Aan de kassa'))
	)
	payment_method = CharField(
		max_length=8, choices=payment_method_choices, default=TRANSFER)

	def total_price(self):
		return sum([ticket.price_category.price for ticket in self.ticket_set.all()])

	def __unicode__(self):
		return u"Online order by {} {} on {}.".format(
			self.first_name, self.last_name, self.date)


class Ticket(Model):
	"""
	A ticket for a certain performance, in a certain price category
	and part of a certain order.
	"""
	performance = ForeignKey(Performance)
	price_category = ForeignKey(PriceCategory)
	order = ForeignKey(Order)

	def __unicode__(self):
		return u'Ticket of € {} for {}, part of [{}]'.format(
			self.price_category.price, self.performance, self.order)
