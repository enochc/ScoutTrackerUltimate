from django.conf.urls import patterns, include, url
from django.conf import settings

from utils.views import oauth_callback, anon_home


urlpatterns = patterns('award.views',
  
    url(r'^list/', 'award_list'),
)