from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('requirement.views',
    url(r'^set/(?P<req_id>\d+)/(?P<user_id>\w+)', 'req_set', name='req_set'),
    url(r'^info/(?P<req_id>\d+)/', 'req_info', name='req_info'),
    )