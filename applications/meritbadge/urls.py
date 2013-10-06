from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from utils.views import oauth_callback, anon_home


urlpatterns = patterns('meritbadge.views',
  
    url(r'^list/', 'badge_list'),
)