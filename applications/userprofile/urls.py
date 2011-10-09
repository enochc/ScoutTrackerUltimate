from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('userprofile.views',
    url(r'^$', 'userhome', name='userhome'),
    url(r'^home/', 'userhome', name='userhome'),
    url(r'^add_scout/(?P<scout_id>\d)/', 'add_scout', name='add_scout'),
    url(r'^add_scout/', 'add_scout', name='add_scout'),
    
    url(r'^(?P<user_id>\d+)/', 'userhome', name='userhome')
   
    )