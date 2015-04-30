from django.conf.urls import patterns, url
from ticketing.views import space, internal
from postermap.views import add_space_poster, space_posters
from django.views.generic import RedirectView

urlpatterns = patterns('',
	url(r'^$', space.landing, name='space_landing'),
	url(r'^tickets/$', space.MultipageTicketingForm.as_view(space.FORMS), name='start_order'),
	url(r'^musicians/space/tickets?$', internal.my_tickets_dashboard, name='my_tickets_dashboard'),
	url(r'^musicians/tickets/?$', RedirectView.as_view(pattern_name='space_ticketing:my_tickets_dashboard')),
	url(r'^musicians/space/?$', internal.promo_dashboard, name='promo_dashboard'),
	url(r'^musicians/?$', RedirectView.as_view(pattern_name='space_ticketing:promo_dashboard')),
	url(r'^musicians/space/postermap/?$', space_posters, name='space_posters'),
	url(r'^musicians/space/postermap/add$', add_space_poster, name='add_poster'),
	url(r'^musicians/space/tickets/add$', internal.register_sold_tickets, name='register_sold_tickets'),
)