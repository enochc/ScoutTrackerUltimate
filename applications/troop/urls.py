from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('troop.views',
    url(r'^$', 'troopHome', name='troop_home'),
    url(r'^home/', 'troopHome', name='troop_home'),
    url(r'^overview/', 'troopOverview', name='troop_overview'),
    url(r'^calendar/', direct_to_template, {'template':'troop/calendar.html'}),
    )