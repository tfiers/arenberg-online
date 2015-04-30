from django.shortcuts import render
from datetime import date
from ticketing.models import Ticket, Performance
from polls.models import ZaventemTransport
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from datetime import date, datetime
from pytz import utc
from pprint import pformat
from core.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ticketing.models import Order, Ticket, Performance, PriceCategory, StandardMarketingPollAnswer
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions
from django.forms import ( Form, ChoiceField, IntegerField, NullBooleanField, CharField)

@login_required
def promo_dashboard(request):
	do = Performance.objects.get(date__contains=date(2015,5,7))
	vr = Performance.objects.get(date__contains=date(2015,5,8))
	data = {
		'num_do' : Ticket.objects.filter(order__performance=do).count(),
		'num_vr' : Ticket.objects.filter(order__performance=vr).count(),
		'num_by_musician_do' : Ticket.objects.filter(order__performance=do, order__standardmarketingpollanswer__referred_member=request.user).count(),
		'num_by_musician_vr' : Ticket.objects.filter(order__performance=vr, order__standardmarketingpollanswer__referred_member=request.user).count(),
		
	}
	return render(request, 'internal/promo_dashboard.html', data)

@login_required
def my_tickets_dashboard(request):
	transport_chosen = (ZaventemTransport.objects.filter(musician=request.user).count() > 0)
	return render(request, 'internal/my_tickets_dashboard.html', {'display_CTA': not transport_chosen})




performances = (
	('do', _('Donderdag 7 mei')),
	('vr', _('Vrijdag 8 mei')),
)


class ReportedSaleForm(Form):
	performance = ChoiceField(required=True, choices=performances)
	num_culture_card_tickets = IntegerField(required=False, min_value=0, initial=0)
	num_student_tickets = IntegerField(required=False, min_value=0, initial=0)
	num_non_student_tickets = IntegerField(required=False, min_value=0, initial=0)
	payment_method = ChoiceField(required=False, choices=Order.payment_method_choices)
	marketing_feedback = CharField(required=False)
	first_concert = NullBooleanField(required=False)
	remarks = CharField(required=False)
	helper = FormHelper()
	helper.layout = Layout(
		'performance',
		'num_student_tickets',
		'num_non_student_tickets',
		'num_culture_card_tickets',
		'first_concert',
		'marketing_feedback',
		'remarks',
		FormActions(
			Submit('submit', _('Registreer'), css_class="btn-success"),
		),
	)


@login_required
def register_sold_tickets(request):
	if request.method == 'POST':
		form = ReportedSaleForm(request.POST)
		if form.is_valid():
			persist_data(parse_form_data(form.cleaned_data), request.user)
			return HttpResponseRedirect(reverse('thanks'))
	else:
		form = ReportedSaleForm()

	return render(request, 'internal/register_sold_tickets.html', {'form': form})

def parse_form_data(form):
	data = {}
	data['performance']              = form.get('performance', '')
	data['performance_full']		 = dict(performances).get(data['performance'], '')
	data['num_culture_card_tickets'] = int(form.get('num_culture_card_tickets', 0))
	data['num_student_tickets']      = int(form.get('num_student_tickets', 0))
	data['num_non_student_tickets']  = int(form.get('num_non_student_tickets', 0))
	data['payment_method']           = form.get('payment_method', '')
	data['payment_method_full']		 = dict(Order.payment_method_choices).get(data['payment_method'], '')
	data['marketing_feedback']       = form.get('marketing_feedback', '')
	data['first_concert'] 			 = form.get('first_concert', None)
	data['remarks']                  = form.get('remarks', '')

	data['total_tickets'] = data['num_student_tickets'] + data['num_non_student_tickets'] + data['num_culture_card_tickets']
	data['total_price'] = 5*data['num_student_tickets'] + 9*data['num_non_student_tickets'] + 4*data['num_culture_card_tickets']

	return data

def persist_data(data, user):
	day_mapping = {'do': 7, 'vr': 8} # ..th of May
	performance = Performance.objects.get(date__contains=date(2015,5,day_mapping[data['performance']]))
		
	order = Order.objects.create(
		performance = performance,
		seller = user,
		date = datetime.now(utc),
		payment_method = data['payment_method'],
		user_remarks = data['remarks'],
		online = False,
	)
	marketing_poll_answers = StandardMarketingPollAnswer.objects.create(
		associated_order = order,
		marketing_feedback = data['marketing_feedback'],
		first_concert = data['first_concert'],
	)

	for i in range(data['num_student_tickets']):
		Ticket.objects.create(
			order = order,
			price_category = PriceCategory.objects.get(name="Student in VVK (vanaf winter 2014)", price=5),
		)
	for i in range(data['num_non_student_tickets']):
		Ticket.objects.create(
			order = order,
			price_category = PriceCategory.objects.get(name="Niet-student in VVK (vanaf winter 2014)", price=9),
		)
	for i in range(data['num_culture_card_tickets']):
		Ticket.objects.create(
			order = order,
			price_category = PriceCategory.objects.get(name="Cultuurkaart in VVK (vanaf winter 2014)", price=4),
		)