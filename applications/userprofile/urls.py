from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('userprofile.views',
    url(r'^$', 'userhome', name='userhome'),
    url(r'^home/', 'userhome', name='userhome'),
    url(r'^add_scout/', 'add_scout', name='add_scout')
   
    )