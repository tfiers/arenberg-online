from django.conf.urls import patterns, url
from ticketing.views import internal, snowman2016, lente2016
from postermap.views import add_poster, posters
from django.views.generic import RedirectView

urlpatterns = patterns('',
	url(r'^$', snowman2016.landing, name='snow_landing'),
	url(r'^tickets/snowman$', snowman2016.MultipageTicketingForm.as_view(snowman2016.FORMS), name='start_order_snow'),
	url(r'^tickets/lente$', lente2016.MultipageTicketingForm.as_view(lente2016.FORMS), name='start_order_lente'),
	url(r'^musicians/concert/tickets?$', internal.my_tickets_dashboard, name='my_tickets_dashboard'),
	url(r'^musicians/concert/registertickets?$', internal.register_sold_tickets, name='register_sold_tickets'),
	url(r'^musicians/concert/?$', internal.promo_dashboard, name='promo_dashboard'),
	url(r'^musicians/concert/postermap/?$', posters, name='posters'),
	url(r'^musicians/concert/postermap/add$', add_poster, name='add_poster'),
	url(r'^musicians/concert/pictures$', internal.facebook_pictures, name='facebook_pictures'),
)
