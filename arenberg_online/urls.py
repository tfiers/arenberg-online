from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from solid_i18n.urls import solid_i18n_patterns
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from axes.decorators import watch_login #needed to activate axes on the login template/view

urlpatterns = patterns ('',
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^setlang/(?P<lang>[\w-]+)/$', 'core.views.set_lang', name='set_lang'), #change lang
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
)

urlpatterns += solid_i18n_patterns('',
    #ALL SPECIAL APP URL INCLUDES FOR THEIR URLS.PY FILES
    url(r'^', include('ticketing.urls', namespace='ticketing')),
    # url(r'^musicians/polls', include('polls.urls', namespace='polls')),
    url(r'^home/', include('ticketing.urls', namespace='ticketing')), #landing page next concert is homepage (doesn't add anything to url in ticketing.urls.py)
    url(r'^schattenjacht/', include(admin.site.urls)),
    #CORE URLS, core is the default app where everything goes that doesn't belong anywhere else
    url(r'^wie$', 'core.views.home', name='wie'), #will render the Arenbergorkest.htm introductory page
    url(r'^sponsors$', 'core.views.sponsors', name='sponsors'), 
    url(r'^contact$', 'core.views.contact', name='contact'),
    url(r'^contact/sent$', 'core.views.contact_sent', name='contact_sent'),
    url(r'^accessrestricted$', 'core.views.notapproved', name='notapproved'), 
    #CORE login related content
    # url(r'^musicians/reset/mailsent/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^musicians/reset/newpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^musicians/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    # url(r'^musicians/reset$',auth_views.password_reset,{'from_email':'noreply@arenbergorkest.be',
    #     'html_email_template_name':'registration/password_reset_mail.html'}, name="iforgotitagain"),
    # url(r'^musicians/choose-password$', 'core.views.change_password', name='change_password'),
    # url(r'^musicians/choose-password/done$', 'core.views.password_set', name='pass_changed'),
    # url(r'^musicians/calendar$', 'core.views.repcalendar', name='calendar'),
    # #using multiple urls for musicianlist, routing
    # url(r'^musicians/list$', 'core.views.musicianlist', name='musicianlist'), 
    # url(r'^musicians/list/(?P<sort>fname|lname|datebirth|phone|study|mail|group)$', 'core.views.musicianlist', name='musicianlist'),
    # url(r'^musicians/list/(?P<sort>fname|lname|datebirth|phone|study|mail|group)/(?P<order>reverse)$','core.views.musicianlist', name='musicianlist'),
    # url(r'^musicians/edit$', 'core.views.edit', name='edit'),
    # url(r'^musicians/calendarview/(?P<pYear>\d+)/(?P<pMonth>\d+)/$', 'core.views.calendarview', name="calendarview"), #regex url dispatcher for calendar
    # url(r'^musicians/calendarview$', 'core.views.calendarview', name='calendarview'),
    # url(r'^musicians/calendarview/add$', 'core.views.calendarview_add', name='calendarview_add'),
    # url(r'^musicians/login$', watch_login(auth_views.login), name='login'),
    # url(r'^musicians/ciao$', auth_views.logout, name='logout'),
    # url(r'^musicians/stop$', 'core.views.axed', name='axed'),
    # url(r'^musicians/register$','core.views.register', name='register'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #needed for user avatars

