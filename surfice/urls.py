from django.conf.urls import patterns, url
from surfice import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index))