from django.conf.urls import patterns, url
from surfice import views

# Delete when deploying!
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	(r'^ding/$', views.ding),
	#url(r'^about/$', views.about, name='about'),
	# surf_url is passed to the surf method in views.py
	# regex to look for any sequence of alphanumeric characters
	# and underscores before the trailing slash
	url(r'^surf/(?P<surf_url>\w+)/$', views.surf, name='surf'))
