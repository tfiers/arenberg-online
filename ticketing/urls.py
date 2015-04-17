from django.conf.urls import patterns, url
from ticketing.views import space

urlpatterns = patterns('',
	url(r'^$', space.landing, name='space_landing'),
	url(r'^tickets/$', space.MultipageTicketingForm.as_view(space.FORMS), name='space_start_order'),
	# url(r'^tickets$', space.start_order, name='space_start_order'),
	# url(r'^tickets/complete-order$', space.complete_order, name='space_complete_order'),
	# url(r'^tickets/thanks$', space.thanks, name='space_thanks'),
)