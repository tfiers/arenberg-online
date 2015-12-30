from django.conf.urls import patterns, url
from music_suggestions import views

urlpatterns = patterns('',
	url(r'^$', views.browse_suggested_pieces, name='browse'),
	url(r'^/(?P<titlelike>.*)/$', views.browse_suggested_pieces, name='browse'),
	url(r'^add$', views.suggest_piece, name='suggest'),
	url(r'^/feature/add$', views.suggest_feature, name='suggest_feature'),
	url(r'^/feature$', views.browse_features, name='browse_feature'),
)