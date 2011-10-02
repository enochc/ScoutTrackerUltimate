from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('troop.views',
    url(r'^$', 'troopHome', name='troop_home'),
    url(r'^home/', 'troopHome', name='troop_home'),
   
    )