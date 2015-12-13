# coding: utf-8

from django.forms import (
	Form, IntegerField, CharField, EmailField, ChoiceField, NullBooleanField )
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from datetime import date, datetime
from pytz import utc
from copy import copy
from pprint import pformat
from core.models import User
from ticketing.models import Order, Ticket, Performance, PriceCategory, StandardMarketingPollAnswer

def landing(request):
	return render(request, 'bal/landing.html')

performances = (
	('di', _('Dinsdag 1 december - om 20u30 in Aula Pieter De Somer, Leuven')),
	('zo', _('Zondag 6 december - om 19u00 in Aula Pieter De Somer, Leuven')),
)

class SpaceTicketingForm_1(Form):
	performance = ChoiceField(required=True, choices=performances)
	num_culture_card_tickets = IntegerField(required=False, min_value=0)
	num_student_tickets = IntegerField(required=False, min_value=0)
	num_non_student_tickets = IntegerField(required=False, min_value=0)
	num_zaventem_tickets = IntegerField(required=False, min_value=0)
	first_name = CharField(required=True)
	last_name = CharField(required=True)
	email = EmailField(required=True)

def get_user_list():
	choices = []
	for user in User.objects.all().order_by('first_name'):
		choices.append((str(user.id), user.get_full_name()))
	return choices

class SpaceTicketingForm_2(Form):
	payment_method = ChoiceField(required=True, choices=Order.payment_method_choices)
	marketing_feedback = CharField(required=True)
	referred_member = ChoiceField(required=False, choices=get_user_list())
	first_concert = NullBooleanField(required=False)
	remarks = CharField(required=False)

def parse_form_data(form):
	data = {}
	data['performance']              = form.get('performance', '')
	data['performance_full']		 = dict(performances).get(data['performance'], '')
	data['num_culture_card_tickets'] = int(form.get('num_culture_card_tickets', 0))
	data['num_student_tickets']      = int(form.get('num_student_tickets', 0))
	data['num_non_student_tickets']  = int(form.get('num_non_student_tickets', 0))
	data['first_name']               = form.get('first_name', '')
	data['last_name']                = form.get('last_name', '')
	data['email']                    = form.get('email', '')
	data['payment_method']           = form.get('payment_method', '')
	data['payment_method_full']		 = dict(Order.payment_method_choices).get(data['payment_method'], '')
	data['marketing_feedback']       = form.get('marketing_feedback', '')
	data['referred_member']          = form.get('referred_member', '')
	data['first_concert'] 			 = form.get('first_concert', None)
	data['remarks']                  = form.get('remarks', '')


	data['total_tickets'] = data['num_student_tickets'] + data['num_non_student_tickets'] + data['num_culture_card_tickets']
	data['total_price'] = 5*data['num_student_tickets'] + 9*data['num_non_student_tickets'] + 4*data['num_culture_card_tickets']

	return data


def persist_data(data):
	day_mapping = {'di': 1, 'zo': 6} # ..th of December
	performance = Performance.objects.get(date__contains=date(2015,12,day_mapping[data['performance']]))
		
	order = Order.objects.create(
		performance = performance,
		first_name = data['first_name'],
		last_name = data['last_name'],
		email = data['email'],
		date = datetime.now(utc),
		payment_method = data['payment_method'],
		user_remarks = data['remarks'],
	)
	if data['referred_member']:
		rm = User.objects.get(id=int(data['referred_member']))
	else:
		rm = None
	marketing_poll_answers = StandardMarketingPollAnswer.objects.create(
		associated_order = order,
		marketing_feedback = data['marketing_feedback'],
		referred_member = rm,
		first_concert = data['first_concert'],
	)

	for i in range(data['num_student_tickets']):
		Ticket.objects.create(
			order = order,
			price_category = PriceCategory.objects.get(full_name="Student VVK (vanaf winter 2014)", price=5),
		)
	for i in range(data['num_non_student_tickets']):
		Ticket.objects.create(
			order = order,
			price_category = PriceCategory.objects.get(full_name="Niet-student in VVK (vanaf winter 2014)", price=9),
		)
	for i in range(data['num_culture_card_tickets']):
		Ticket.objects.create(
			order = order,
			price_category = PriceCategory.objects.get(full_name="KU Leuven Cultuurkaart in VVK (vanaf winter 2014)", price=4),
		)

# from django.conf import settings
# import os
# import requests
# def send_mail_temp(subject, msg, fromm, to, html_message):
# 	with open(os.path.join(settings.BASE_DIR, 'arenberg-secure/mailgun_api_key')) as f:
# 		print(requests.post(
# 	        "https://api.mailgun.net/v3/arenbergorkest.be/messages",
# 	        auth=("api", f.read().strip()),
# 	        data={"from": fromm,
# 	              "to": to,
# 	              "subject": subject,
# 	              "text": msg,
# 	              "html": html_message,}))

def email_user(data):
	subject = "Bestelling tickets 'Bal Masqué' concert Arenbergorkest"
	msg = render_to_string('bal/email.html', data)
	fromm = "Arenbergorkest <webapp@arenbergorkest.be>"
	send_mail(subject, msg, fromm, [data['email']], html_message=msg)
	send_mail(subject, msg, fromm, ['tomas.fiers@gmail.com'], html_message=msg)

FORMS = [("start_order", SpaceTicketingForm_1),
		 ("complete_order", SpaceTicketingForm_2)]

TEMPLATES = {"start_order": "bal/start_order.html",
			 "complete_order": "bal/complete_order.html"}

class MultipageTicketingForm(SessionWizardView):
	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

	def get_context_data(self, form, **kwargs):
		context = super(SessionWizardView, self).get_context_data(form=form, **kwargs)
		if self.steps.current == 'complete_order':
			data = parse_form_data(self.get_cleaned_data_for_step('start_order'))
			context.update({'first_form': data})
		return context
		
	def done(self, form_list, form_dict, **kwargs):
		form_data = copy(form_dict['start_order'].cleaned_data)
		form_data.update(form_dict['complete_order'].cleaned_data)
		data = parse_form_data(form_data)
		persist_data(data)
		#email_user(data)
		# email_admin(data)
		return render_to_response('bal/thanks.html', data)