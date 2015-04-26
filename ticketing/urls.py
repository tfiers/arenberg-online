from django.conf.urls import patterns, url
from ticketing.views import space, internal

urlpatterns = patterns('',
	url(r'^$', space.landing, name='space_landing'),
	url(r'^tickets/$', space.MultipageTicketingForm.as_view(space.FORMS), name='space_start_order'),
	url(r'^musicians/tickets$', internal.musician_tickets, name='musician_tickets'),
)