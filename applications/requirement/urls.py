from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('requirement.views',
    url(r'^$', 'troopHome', name='troop_home'),
    url(r'^set/(?P<req_id>\d+)/(?P<user_id>\w+)', 'req_set', name='req_set'),
    url(r'^overview/', 'troopOverview', name='troop_overview'),
   
    )