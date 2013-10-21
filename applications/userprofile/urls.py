from django.conf.urls import patterns, include, url

urlpatterns = patterns('userprofile.views',
    
    url(r'^home/', 'userhome', name='userhome'),
    url(r'^add_scout/(?P<scout_id>\d+)/', 'add_scout', name='add_scout'),
    url(r'^add_scout/', 'add_scout', name='add_scout'),
    url(r'^add_award/', 'add_award', name='add_award'),
    
    url(r'^set_pos/(?P<user_id>\d+)/(?P<pos_id>\d+)/', 'setUserPosition', name='setUserPosition'),
    url(r'^(?P<user_id>\d+)/', 'userhome', name='userhome'),
    url(r'^$', 'userhome', name='userhome'),
   
    )