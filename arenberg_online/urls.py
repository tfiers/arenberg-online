from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from solid_i18n.urls import solid_i18n_patterns
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns ('',
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^setlang/(?P<lang>[\w-]+)/$', 'core.views.set_lang', name='set_lang'), #change lang
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
)

urlpatterns += solid_i18n_patterns('',
    #first include all SPECIAL app url.py files
    url(r'^', include('ticketing.urls', namespace='ticketing')),
    url(r'^musicians/polls', include('polls.urls', namespace='polls')),
    url(r'^home/', include('ticketing.urls', namespace='ticketing')), #landing page next concert is homepage (doesn't add anything to url in ticketing.urls.py)
    url(r'^admin/', include(admin.site.urls)),
    #then the URL's for the main app CORE
    url(r'^wie$', 'core.views.home', name='wie'), #will render the Arenbergorkest.htm introductory page
    url(r'^sponsors$', 'core.views.sponsors', name='sponsors'), 
    url(r'^contact$', 'core.views.contact', name='contact'),
    url(r'^contact/sent$', 'core.views.contact_sent', name='contact_sent'),
    url(r'^accessrestricted$', 'core.views.notapproved', name='notapproved'), 
    #next three have to be here, because of the names. if they're in core/urls.py the names are musicians:... and contrib.auth won't recognise them
    url(r'^musicians/reset/mailsent/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^musicians/reset/newpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^musicians/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #moved here so @user_passes tests correctly go to this page, if it's musicians/accesrestricted it always becomes musicians/musicians/accesestricted and then url not found
    url(r'^musicians/', include('core.urls', namespace='musicians')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #needed for user avatars

