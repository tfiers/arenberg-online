from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'arenberg_online.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tickets/', include('ticketing.urls', namespace='ticketing')),
    url(r'^', include('music_suggestions.urls', namespace='music_suggestions_base')),
    url(r'^music_suggestions/', include('music_suggestions.urls', namespace='music_suggestions')),
)
