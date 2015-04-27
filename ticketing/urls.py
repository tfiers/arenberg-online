from django.conf.urls import patterns, url
from ticketing.views import space, internal
from postermap.views import add_space_poster
from django.views.generic import RedirectView

urlpatterns = patterns('',
	url(r'^$', space.landing, name='space_landing'),
	url(r'^tickets/$', space.MultipageTicketingForm.as_view(space.FORMS), name='start_order'),
	url(r'^musicians/space$', internal.musician_dashboard, name='musician_dashboard'),
	url(r'^musicians/tickets$', RedirectView.as_view(pattern_name='musician_dashboard')),
	url(r'^musicians/?$', RedirectView.as_view(pattern_name='musician_dashboard')),
	url(r'^musicians/space/postermap(/add)?$', add_space_poster, name='add_space_poster'),
)