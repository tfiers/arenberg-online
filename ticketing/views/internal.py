from django.shortcuts import render
from datetime import date
from ticketing.models import Ticket, Performance

def musician_tickets(request):
	do = Performance.objects.get(date__contains=date(2015,5,7))
	vr = Performance.objects.get(date__contains=date(2015,5,8))
	num_do = Ticket.objects.filter(order__performance=do).count()
	num_vr = Ticket.objects.filter(order__performance=vr).count()
	return render(request, 'internal/musician_dashboard.html', {'num_do': num_do,'num_vr': num_vr})