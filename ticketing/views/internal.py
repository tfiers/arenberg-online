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
from ticketing.models import ( Order, Ticket, Performance, PriceCategory, 
	StandardMarketingPollAnswer, GivenPaperTickets )
from django.forms import ( Form, ChoiceField, IntegerField, NullBooleanField, 
	CharField, DateTimeField)
from django.contrib import messages
import django.utils.timezone as django_tz
from django.db.models import Q

@login_required
def promo_dashboard(request):
	do = Performance.objects.get(date__contains=date(2015,5,7))
	vr = Performance.objects.get(date__contains=date(2015,5,8))
	za = Performance.objects.get(date__contains=date(2015,5,9))
	data = {
		'num_do' : Ticket.objects.filter(order__performance=do).count(),
		'num_vr' : Ticket.objects.filter(order__performance=vr).count(),
		'num_za' : Ticket.objects.filter(order__performance=za).count(),
		# 'num_by_musician_do' : Ticket.objects.filter(order__performance=do, order__standardmarketingpollanswer__referred_member=request.user).count(),
		# 'num_by_musician_vr' : Ticket.objects.filter(order__performance=vr, order__standardmarketingpollanswer__referred_member=request.user).count(),
	}
	total_graph, thu_graph, fri_graph = [], [], []
	total_tickets, thu_tickets, fri_tickets = 0, 0, 0
	for order in sorted(Order.objects.exclude(performance=za), key=lambda o: o.creation_date):
		total_tickets += order.num_tickets()
		total_graph.append({
			'timestamp': to_timestamp(order.creation_date),
			'num_new_tickets': order.num_tickets(),
			'total_tickets': total_tickets,
			'order': order,
		})
		if order.performance == do:
			thu_tickets += order.num_tickets()
			thu_graph.append({
				'timestamp': to_timestamp(order.creation_date),
				'num_new_tickets': order.num_tickets(),
				'total_tickets': thu_tickets,
				'order': order,
			})
		elif order.performance == vr:
			fri_tickets += order.num_tickets()
			fri_graph.append({
				'timestamp': to_timestamp(order.creation_date),
				'num_new_tickets': order.num_tickets(),
				'total_tickets': fri_tickets,
				'order': order,
			})
	data['total_graph'] = total_graph
	data['thu_graph'] = thu_graph
	data['fri_graph'] = fri_graph

	user_totals = []
	for user in User.objects.all():
		user_totals.append({
			'user': user,
			'num_tickets': Ticket.objects.filter(
				Q(order__seller=user) | 
				Q(order__standardmarketingpollanswer__referred_member=user)).count()
		})
	data['user_totals'] = sorted(user_totals, key=lambda obj: -obj['num_tickets'])[0:5]

	return render(request, 'internal/promo_dashboard.html', data)

def to_timestamp(dt):
	epoch = django_tz.make_aware(datetime(1970,1,1), django_tz.get_default_timezone())
	return int((dt - epoch).total_seconds()*1000)

@login_required
def facebook_pictures(request):
	return render(request, 'internal/pictures.html', {})

@login_required
def my_tickets_dashboard(request):
	data = {}

	transport_chosen = (ZaventemTransport.objects.filter(musician=request.user).count() > 0)
	data['display_CTA'] = not transport_chosen

	data['ticket_distributions'] = \
		GivenPaperTickets.objects.filter(given_to=request.user)
	data['total_tickets_given'] = \
		sum([ts.count for ts in GivenPaperTickets.objects.filter(given_to=request.user)])

	data['registered_sales'] = \
		Order.objects.filter(online=False, seller=request.user)
	data['total_tickets_registered_sales'] = \
		Ticket.objects.filter(order__online=False, order__seller=request.user).count()
	data['total_price_registered_sales'] = \
		sum([o.total_price() for o in Order.objects.filter(online=False, seller=request.user)])
		
	data['online_order_mentioneds'] = \
		Order.objects.filter(online=True, standardmarketingpollanswer__referred_member=request.user)
	data['total_tickets_online_order_mentioneds'] = \
		Ticket.objects.filter(order__online=True, order__standardmarketingpollanswer__referred_member=request.user).count()
		
	return render(request, 'internal/my_tickets_dashboard.html', data)

performances = (
	('do', _('Donderdag 7 mei')),
	('vr', _('Vrijdag 8 mei')),
)

class ReportedSaleForm(Form):
	performance = ChoiceField(required=True, choices=performances)
	num_student_tickets = IntegerField(required=False, min_value=0, initial=0)
	num_non_student_tickets = IntegerField(required=False, min_value=0, initial=0)
	num_culture_card_tickets = IntegerField(required=False, min_value=0, initial=0)
	payment_method = ChoiceField(required=False, choices=Order.payment_method_choices)
	marketing_feedback = CharField(required=False)
	first_concert = NullBooleanField(required=False)
	sale_date = DateTimeField(required=False)
	remarks = CharField(required=False)

@login_required
def register_sold_tickets(request):
	if request.method == 'POST':
		form = ReportedSaleForm(request.POST)
		if form.is_valid():
			persist_data(parse_form_data(form.cleaned_data), request.user)
			messages.success(request, _('Je verkochte tickets zijn geregistreerd.'))
			return HttpResponseRedirect(reverse('space_ticketing:my_tickets_dashboard'))
	else:
		form = ReportedSaleForm(initial={'sale_date': datetime.now().strftime('%Y-%m-%d %H:%M')})

	return render(request, 'internal/register_sold_tickets.html', {'form': form})

def parse_form_data(form):
	data = {}
	data['performance']              = form.get('performance', '')
	data['performance_full']		 = dict(performances).get(data['performance'], '')
	data['num_culture_card_tickets'] = int(form.get('num_culture_card_tickets', 0))
	data['num_student_tickets']      = int(form.get('num_student_tickets', 0))
	data['num_non_student_tickets']  = int(form.get('num_non_student_tickets', 0))
	data['marketing_feedback']       = form.get('marketing_feedback', '')
	data['first_concert'] 			 = form.get('first_concert', None)
	data['sale_date'] 			 	 = form.get('sale_date', None)
	data['remarks']                  = form.get('remarks', '')

	return data

def persist_data(data, user):
	day_mapping = {'do': 7, 'vr': 8} # ..th of May
	performance = Performance.objects.get(date__contains=date(2015,5,day_mapping[data['performance']]))
		
	order = Order.objects.create(
		performance = performance,
		seller = user,
		sale_date = data['sale_date'],
		payment_method = None,
		date = datetime.now(utc),
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