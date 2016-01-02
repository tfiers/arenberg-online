from django.conf.urls import patterns, url
from core import views
from django.contrib.auth import views as auth_views
from axes.decorators import watch_login #needed to activate axes on the login template/view

urlpatterns = patterns('',
	#all pages involving authentication or with authentication required (except for ticketing and poll pages, the ones that belong in a seperate app)
    url(r'^choose-password$', 'core.views.change_password', name='change_password'),
    url(r'^choose-password/done$', 'core.views.password_set', name='pass_changed'),
    url(r'^calendar$', 'core.views.repcalendar', name='calendar'),
    url(r'^list$', 'core.views.musicianlist', name='musicianlist'),
    url(r'^edit$', 'core.views.edit', name='edit'),
    url(r'^calendarview/(?P<pYear>\d+)/(?P<pMonth>\d+)/$', 'core.views.calendarview', name="calendarview"), #regex url dispatcher for calendar
    url(r'^calendarview$', 'core.views.calendarview', name='calendarview'),
    url(r'^calendarview/add$', 'core.views.calendarview_add', name='calendarview_add'),
    url(r'^login$', watch_login(auth_views.login), name='login'),
    url(r'^adieu$', auth_views.logout, name='logout'),
    url(r'^stop$', 'core.views.axed', name='axed'),
    url(r'^register$','core.views.register', name='register'),
)