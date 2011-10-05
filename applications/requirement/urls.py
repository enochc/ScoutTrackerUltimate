from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('requirement.views',
    url(r'^set/(?P<req_id>\d+)/(?P<user_id>\w+)', 'req_set', name='req_set'),
    url(r'^info/(?P<req_id>\d+)/', 'req_info', name='req_info'),
    url(r'^rank_requirements/(?P<rank_id>\d+)/', 'rank_requirements', name='rank_requirements'),
    )