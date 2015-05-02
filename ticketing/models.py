# coding: utf-8

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import get_current_timezone
from django.db.models import (
	Model, ForeignKey, OneToOneField, ManyToManyField,CharField, DateTimeField, 
	FloatField, NullBooleanField, EmailField, DateTimeField, TextField, BooleanField )
from core.models import User




# ---------------------------- CORE MODELS -----------------------------------

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
	date = DateTimeField(_('datum en eventueel uur'), blank=True, null=True)
	location = CharField(max_length=200, blank=True)
	price_categories = ManyToManyField('PriceCategory')

	def __unicode__(self):
		return u'"{}" on {:%a %b %d %H:%M} @ {}'.format(
			self.production.name, self.date, self.location)


class PriceCategory(Model):
	"""
	A named price class for tickets.
	For example: "Students with a culture card (pre sale)", € 4
	"""
	name = CharField(max_length=200, unique=True)
	price = FloatField()

	def __unicode__(self):
		return u'"{}": € {:g}'.format(self.name, self.price)

	class Meta:
		verbose_name_plural = "price categories"


class Order(Model):
	"""
	Created when someone orders tickets online for a certain performance.
	Created when an orchestra member reports having sold paper tickets.
	"""
	performance = ForeignKey(Performance)
	first_name = CharField(max_length=75, blank=True, null=True)
	last_name = CharField(max_length=75, blank=True, null=True)
	email = EmailField(blank=True, null=True)
	date = DateTimeField(_("datum van online bestelling"))
	TRANSFER, CASH = 'transfer', 'cash'
	payment_method_choices = (
		(TRANSFER, _('Via overschrijving')), (CASH, _('Aan de kassa')))
	payment_method = CharField(
		max_length=8, choices=payment_method_choices, default=TRANSFER)
	user_remarks = TextField(blank=True, null=True, help_text=_(
		'opmerkingen gebruiker. Voor vragen en speciale verzoeken.'))
	admin_remarks = TextField(blank=True, null=True)
	online = BooleanField(default=True) # True = online, False = musician reported a sale
	seller = ForeignKey(User, null=True, blank=True)

	def num_tickets(self):
		return len(self.ticket_set.all())

	def total_price(self):
		return sum([ticket.price_category.price for ticket in self.ticket_set.all()])

	def __unicode__(self):
		if self.online:
			return u"Online order by {} {} on {:%d-%m-%Y %H:%M:%S}.".format(
				self.first_name, self.last_name, self.date.astimezone(get_current_timezone()))
		else:
			return u"Ticket sale by {} on {:%d-%m-%Y %H:%M:%S}.".format(
				self.seller, self.date.astimezone(get_current_timezone()))

class Ticket(Model):
	"""
	A ticket in a certain price category and part of a certain order.
	"""
	price_category = ForeignKey(PriceCategory)
	order = ForeignKey(Order)

	def __unicode__(self):
		return u'Ticket of € {:g} for {}, part of [{}]'.format(
			self.price_category.price, self.order.performance, self.order)




# ---------------------------- EXTRA MODELS -----------------------------------

class MarketingPollAnswer(Model):
	pass

class StandardMarketingPollAnswer(MarketingPollAnswer):
	''' For asking marketing questions to people that are
		ordering tickets for a concert. '''
	associated_order = OneToOneField(Order)
	marketing_feedback = TextField(blank=True, help_text=_(
		'Voor antwoorden op de vraag: "Hoe heb je van dit concert gehoord?"'))
	referred_member = ForeignKey(User, blank=True, null=True, help_text=_(
		'Ken je een muzikant en kom je dankzij hem of haar luisteren?'))
	first_concert = NullBooleanField()

	def __unicode__(self):
		return u'Marketing poll answers of {}'.format(self.associated_order)