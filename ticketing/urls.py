from django.conf.urls import patterns, url
from ticketing.views import internal, snowman2016
from postermap.views import add_space_poster, space_posters
from django.views.generic import RedirectView

urlpatterns = patterns('',
	url(r'^$', snowman2016.landing, name='snow_landing'),
	url(r'^tickets/snowman$', snowman2016.MultipageTicketingForm.as_view(snowman2016.FORMS), name='start_order_snow'),
	#url(r'^musicians/bal/tickets?$', internal.my_tickets_dashboard, name='my_tickets_dashboard'),
	#url(r'^musicians/tickets/?$', RedirectView.as_view(pattern_name='bal_ticketing:my_tickets_dashboard')),
	#url(r'^musicians/bal/?$', internal.promo_dashboard, name='promo_dashboard'),
	#url(r'^musicians/?$', RedirectView.as_view(pattern_name='bal_ticketing:promo_dashboard')),
	#url(r'^musicians/bal/postermap/?$', space_posters, name='bal_posters'),
	#url(r'^musicians/bal/postermap/add$', add_space_poster, name='add_poster'),
	#url(r'^musicians/bal/pictures$', internal.facebook_pictures, name='facebook_pictures'),
)
