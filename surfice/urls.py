from django.conf.urls import patterns, url
from surfice import views, ajax

# Delete when deploying!
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^admin/$', views.admin, name='admin'),
	url(r'^admin/ajax/(?P<action>[^/]*)', ajax.ajax, name='ajax'),
	#url(r'^ajax', ajax.ajax, name='ajax'), # No params
	#url(r'^about/$', views.about, name='about'),
	# surf_url is passed to the surf method in views.py
	# regex to look for any sequence of alphanumeric characters
	# and underscores before the trailing slash
	url(r'^surf/(?P<surf_url>\w+)/$', views.surf, name='surf'),
	
	
	#temp
	#url(r'^surfs.html', views.surfs, name='surfs'),
	#url(r'^surfices.html', views.surfices, name='surfices'),
	#url(r'^settings.html', views.settings, name='settings'),
	#url(r'^status.html', views.status, name='status'),
)
