from django.conf.urls import patterns, url
from music_suggestions import views

urlpatterns = patterns('',
	url(r'^$', views.browse_suggested_pieces, name='browse'),
	url(r'^add$', views.suggest_piece, name='suggest'),
)