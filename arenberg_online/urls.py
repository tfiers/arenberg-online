from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from solid_i18n.urls import solid_i18n_patterns
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns ('',
    url(r'^setlang/(?P<lang>[\w-]+)/$', 'core.views.set_lang', name='set_lang'),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
)

# See: https://github.com/stochastic-technologies/django-loginas
urlpatterns += patterns('loginas.views',
    url(r"^login/user/(?P<user_id>.+)/$", "user_login", name="loginas-user-login"),
)

urlpatterns += solid_i18n_patterns('',

    url(r'^wie$', 'core.views.home', name='wie'), #will render the Arenbergorkest.htm introductory page
    # Examples:
    # url(r'^$', 'arenberg_online.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('ticketing.urls', namespace='ticketing')),
    url(r'^musicians/suggestions', include('music_suggestions.urls', namespace='suggestions')),
    url(r'^home/', include('ticketing.urls', namespace='ticketing')),
    url(r'^register$','core.views.register', name='register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sponsors$', 'core.views.sponsors', name='sponsors'), #commented out in base.html
    url(r'^contact$', 'core.views.contact', name='contact'), #commented out in base.html
    #url(r'^musicians/music$', 'core.views.list', name='music'), #rudimentary start for files downloadable from server, probably not going to be used so commented out to disable the link
    url(r'^musicians/calendar$', 'core.views.calendar', name='calendar'),
    url(r'^musicians/links$', 'core.views.links', name='links'),
    url(r'^musicians/login$', auth_views.login, name='login'),
    url(r'^musicians/adieu$', auth_views.logout, name='logout'),
    url(r'^musicians/choose-password$', 'core.views.change_default_password', name='change_password'),
    url(r'^musicians/choose-password/done$', 'core.views.password_set', name='pass_changed'),
    url(r'^meer\-orkest$', 'polls.views.new_semester', name="new_semester_poll"),
    url(r'^musicians/naar\-zaventem$', RedirectView.as_view(pattern_name='zaventem_transport_poll')),
    url(r'^naar\-zaventem$', 'polls.views.zaventem_transport', name="zaventem_transport_poll"),
    url(r'^thanks$', 'polls.views.thanks', name="thanks"),
    url(r'^music_suggestions/', include('music_suggestions.urls', namespace='music_suggestions')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #needed for rudimentary start of file upload and download system, probably not going to be used

