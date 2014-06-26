from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'surfstat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^db/', include(admin.site.urls)),
    
    # Root redirects to index
    
    # Root redirects to surfice app
    url('', include('surfice.urls')),
    # Include surfice app
    url(r'^surfice/', include('surfice.urls')),
)
