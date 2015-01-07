from django.conf.urls import patterns, url

from ticketing import views

urlpatterns = patterns('',
	url(r'^$', views.order_snowman_tickets, name='snowman_ticketing'),
	url(r'^thanks$', views.thanks_for_snowman, name='snowman_thanks'),
)