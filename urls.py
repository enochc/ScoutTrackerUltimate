from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from utils.views import oauth_callback, anon_home

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^scouts/', include('scouts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'auth.views.login_view'),
    url(r'^logout/', 'auth.views.logout_view'),
    
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT +'/js'}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT +'/css'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT +'/images'}),

    url(r'^$', anon_home),
    url(r'^user/', include('userprofile.urls')),
    url(r'^troop/', include('troop.urls')),
    url(r'^requirement/', include('requirement.urls')),
    url(r'^meritbadge/', include('meritbadge.urls')),
    url(r'^oauth2callback/', oauth_callback),
    url(r'^register/', oauth_callback),
)
