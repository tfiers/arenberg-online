from django.conf.urls import patterns, url
from polls import views

urlpatterns = patterns('',
	#stel muziek voor, met like systeem
	url(r'^/music$', views.browse_suggested_pieces, name='browse'),
	url(r'^/(?P<titlelike>.*)/$', views.browse_suggested_pieces, name='browse'),
	url(r'^/music/add$', views.suggest_piece, name='suggest'),
	#poll features website
	url(r'^/feature/add$', views.suggest_feature, name='suggest_feature'),
	url(r'^/feature$', views.browse_features, name='browse_feature'),
	#enquete new semester
    url(r'^/meer\-orkest$', views.new_semester, name="new_semester_poll"),
    url(r'^/thanks$', views.thanks, name="thanks"),
)