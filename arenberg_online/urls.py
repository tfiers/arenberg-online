from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from solid_i18n.urls import solid_i18n_patterns
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns ('',
    url(r'^setlang/(?P<lang>[\w-]+)/$', 'core.views.set_lang', name='set_lang'), #change lang
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
)

urlpatterns += solid_i18n_patterns('',
    #first include all app urls and such
    url(r'^', include('ticketing.urls', namespace='ticketing')),
    url(r'^musicians/polls', include('polls.urls', namespace='polls')),
    url(r'^home/', include('ticketing.urls', namespace='ticketing')), #landing page next concert is homepage (doesn't add anything to url in ticketing.urls.py)
    url(r'^musicians', include('core.urls', namespace='musicians')),
    url(r'^admin/', include(admin.site.urls)),
    #general pages, also in core, rendered here so they don't have the musicians prefix
    url(r'^wie$', 'core.views.home', name='wie'), #will render the Arenbergorkest.htm introductory page
    url(r'^sponsors$', 'core.views.sponsors', name='sponsors'), 
    url(r'^contact$', 'core.views.contact', name='contact'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #needed for user avatars

