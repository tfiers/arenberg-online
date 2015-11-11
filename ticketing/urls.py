from django.conf.urls import patterns, url
from ticketing.views import bal, space, internal
from postermap.views import add_space_poster, space_posters
from django.views.generic import RedirectView

urlpatterns = patterns('',
	url(r'^$', bal.landing, name='space_landing'),
	url(r'^tickets/$', bal.MultipageTicketingForm.as_view(bal.FORMS), name='start_order'),
	#url(r'^musicians/bal/tickets?$', internal.my_tickets_dashboard, name='my_tickets_dashboard'),
	#url(r'^musicians/tickets/?$', RedirectView.as_view(pattern_name='bal_ticketing:my_tickets_dashboard')),
	#url(r'^musicians/bal/?$', internal.promo_dashboard, name='promo_dashboard'),
	#url(r'^musicians/?$', RedirectView.as_view(pattern_name='bal_ticketing:promo_dashboard')),
	#url(r'^musicians/bal/postermap/?$', space_posters, name='bal_posters'),
	#url(r'^musicians/bal/postermap/add$', add_space_poster, name='add_poster'),
	#url(r'^musicians/bal/pictures$', internal.facebook_pictures, name='facebook_pictures'),
	url(r'^musicians/bal/tickets/add$', internal.register_sold_tickets, name='register_sold_tickets'),
)
