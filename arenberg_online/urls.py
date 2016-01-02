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
    #first include all SPECIAL app url.py files
    url(r'^', include('ticketing.urls', namespace='ticketing')),
    url(r'^musicians/polls', include('polls.urls', namespace='polls')),
    url(r'^home/', include('ticketing.urls', namespace='ticketing')), #landing page next concert is homepage (doesn't add anything to url in ticketing.urls.py)
    url(r'^admin/', include(admin.site.urls)),
    #then the URL's for the main app CORE
    url(r'^wie$', 'core.views.home', name='wie'), #will render the Arenbergorkest.htm introductory page
    url(r'^sponsors$', 'core.views.sponsors', name='sponsors'), 
    url(r'^contact$', 'core.views.contact', name='contact'),
    url(r'^accessrestricted$', 'core.views.notapproved', name='notapproved'), 
    #moved here so @user_passes tests correctly go to this page, if it's musicians/accesrestricted it always becomes musicians/musicians/accesestricted and then url not found
    url(r'^musicians/', include('core.urls', namespace='musicians')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #needed for user avatars

