from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^scouts/', include('scouts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^login/', 'auth.views.login'),
    url(r'^logout/', 'auth.views.logout_view'),
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT +'/js'}),

    url(r'^$', direct_to_template, {'template':'home.html'}),
)
