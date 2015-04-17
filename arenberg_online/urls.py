from django.conf.urls import patterns, include, url
from django.contrib import admin
from solid_i18n.urls import solid_i18n_patterns

urlpatterns = patterns ('',
    url(r'^setlang/(?P<lang>[\w-]+)/$', 'core.views.set_lang', name='set_lang'),
)

urlpatterns += solid_i18n_patterns('',
    # Examples:
    # url(r'^$', 'arenberg_online.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('ticketing.urls', namespace='space_ticketing')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^meer\-orkest$', 'polls.views.new_semester_answer', name="new_semester_poll"),
    url(r'^thanks$', 'polls.views.thanks', name="thanks"),
    url(r'^music_suggestions/', include('music_suggestions.urls', namespace='music_suggestions')),
    url(r'^(?P<path>.*)/$', 'core.views.redirect_to_old_drupal_site', name='redirect_to_old_drupal_site'), # catch-all
)
