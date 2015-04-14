# coding: utf-8

from django.forms import (
	Form, IntegerField, CharField, EmailField, ChoiceField, TextField, NullBooleanField )
from django.shortcuts import render
from django.http import HttpResponseRedirect
import django.utils.timezone as django_tz
from core.models import User
from ticketing.models import Order, Ticket, Performance, PriceCategory

def get_user_list():
	choices = []
	for user in User.objects.all():
		choices += (user.id, user.get_full_name())
	return choices

performances = (
	('do', _('Donderdag 7 mei in Leuven')),
	('vr', _('Vrijdag 8 mei in Leuven')),
	('za', _('Zaterdag 9 mei in Zaventem')),
)

class SpaceTicketingForm_1(Form):
	performance = ChoiceField(required=True, choices=performances)
	num_culture_card_tickets = IntegerField(required=False, initial=0, min_value=0)
	num_student_tickets = IntegerField(required=False, initial=0, min_value=0)
	num_non_student_tickets = IntegerField(required=False, initial=0, min_value=0)
	first_name = CharField(required=True)
	last_name = CharField(required=True)
	email = EmailField(required=True)

class SpaceTicketingForm_2(Form):
	payment_method = ChoiceField(required=True, choices=Order.payment_method_choices)
	marketing_feedback = TextField(required=True)
	referred_member = ChoiceField(required=False, choices=get_user_list)
	first_concert = NullBooleanField(required=True)
	remarks = TextField(required=False)
