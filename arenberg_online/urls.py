from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from solid_i18n.urls import solid_i18n_patterns
from django.views.generic import RedirectView

urlpatterns = patterns ('',
    url(r'^setlang/(?P<lang>[\w-]+)/$', 'core.views.set_lang', name='set_lang'),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
)

# See: https://github.com/stochastic-technologies/django-loginas
urlpatterns += patterns('loginas.views',
    url(r"^login/user/(?P<user_id>.+)/$", "user_login", name="loginas-user-login"),
)

urlpatterns += solid_i18n_patterns('',
    # Examples:
    # url(r'^$', 'arenberg_online.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', 'core.views.home', name='home'), #will render the Arenbergorkest.htm homepage, disable because of concerts
    url(r'^', include('ticketing.urls', namespace='bal_ticketing')),
    url(r'^home/', include('ticketing.urls', namespace='bal_ticketing')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sponsors$', 'core.views.sponsors', name='sponsors'),
    url(r'^contact$', 'core.views.contact', name='contact'),
    url(r'^musicians/login$', auth_views.login, name='login'),
    url(r'^musicians/adieu$', auth_views.logout, name='logout'),
    url(r'^musicians/choose-password$', 'core.views.change_default_password', name='change_password'),
    url(r'^musicians/choose-password/done$', 'core.views.password_set', name='pass_changed'),
    url(r'^meer\-orkest$', 'polls.views.new_semester', name="new_semester_poll"),
    url(r'^musicians/naar\-zaventem$', RedirectView.as_view(pattern_name='zaventem_transport_poll')),
    url(r'^naar\-zaventem$', 'polls.views.zaventem_transport', name="zaventem_transport_poll"),
    url(r'^thanks$', 'polls.views.thanks', name="thanks"),
    url(r'^music_suggestions/', include('music_suggestions.urls', namespace='music_suggestions')),
    url(r'^(?P<path>.*)/$', 'core.views.redirect_to_old_drupal_site', name='redirect_to_old_drupal_site'), # catch-all
)
