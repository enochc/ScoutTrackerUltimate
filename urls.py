from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

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
    url(r'^fblogin/', 'auth.views.fblogin_view'),
    url(r'^logout/', 'auth.views.logout_view'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT +'/js'}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT +'/css'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT +'/images'}),

    url(r'^$', anon_home),
    url(r'^user/', include('userprofile.urls')),
    url(r'^unit/', include('unit.urls')),
    url(r'^requirement/', include('requirement.urls')),
    url(r'^award/', include('award.urls')),
    url(r'^oauth2callback/', oauth_callback),
    url(r'^register/', oauth_callback),
    url(r'^privacy/', TemplateView.as_view(template_name='privacy.html'))
)
