from django.conf.urls import patterns, url
from core import views


urlpatterns = patterns('',
	url(r'^page$', views.register,name='register'), #page becuase otherwise url is /registerregister/
)
