from django.shortcuts import render
from datetime import date
from ticketing.models import Ticket, Performance
from polls.models import ZaventemTransport
from django.contrib.auth.decorators import login_required

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