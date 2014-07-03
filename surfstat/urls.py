from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'surfstat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^db/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'surfice/base_login.html'} ),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    
    # Root redirects to index
    
    # Root redirects to surfice app
    url('', include('surfice.urls')),
    # Include surfice app
    url(r'^surfice/', include('surfice.urls')),
)
