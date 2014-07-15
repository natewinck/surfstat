from django.conf.urls import patterns, url
from surfice import views, ajax

# Delete when deploying!
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
	# Home
	url(r'^$', views.index, name='index'),
	
	#url(r'^ajax', ajax.ajax, name='ajax'), # No params
	#url(r'^about/$', views.about, name='about'),
	# surf_url is passed to the surf method in views.py
	# regex to look for any sequence of alphanumeric characters
	# and underscores before the trailing slash
	#url(r'^surf/(?P<surf_url>\w+)/$', views.surf, name='surf'),
	
	# AJAX
	url(r'^.*?ajax/(?P<action>[^/]*)', ajax.dispatch, name='ajax'),
	
	# Admin
	url(r'^admin/$', views.admin, name='admin'),
	url(r'^admin/surfs/$', views.surfs, name='surfs'),
	url(r'^admin/surfices/$', views.surfices, name='surfices'),
	url(r'^admin/settings/$', views.settings, name='settings'),
	url(r'^admin/statuses/$', views.statuses, name='statuses'),
	
	url(r'^admin/events/(?P<page>\w*)(?:\/)(?P<order_by>[-\w]*)', views.events, name='events'),
	url(r'^admin/events/(?P<page>\w*)', views.events, name='events'),
	
	url(r'^admin/dings/(?P<page>\w*)(?:\/)(?P<order_by>[-\w]*)', views.dings, name='dings'),
	url(r'^admin/dings/(?P<page>\w*)', views.dings, name='dings'),
	url(r'^admin/dings/$', views.dings, name='dings'),
	
	# Need to comment out because I'm not going to use any except ding
	url(r'^admin/surfice/(?P<surfice>.*)/$', views.surfice, name='surfice'),
	url(r'^admin/status/(?P<status>.*)/$', views.status, name='status'),
	url(r'^admin/ding/(?P<ding>.*)', views.ding, name='ding'),
	
	#url(r'^admin/dings/$', views.dings, name='dings'),
	#url(r'^admin/login/$', views.login, name='login'),
)
