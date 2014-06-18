from django.conf.urls import patterns, url
from surfice import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	#url(r'^about/$', views.about, name='about'),
	# surf_url is passed to the surf method in views.py
	# regex to look for any sequence of alphanumeric characters
	# and underscores before the trailing slash
	url(r'^surf/(?P<surf_url>\w+)/$', views.surf, name='surf'))