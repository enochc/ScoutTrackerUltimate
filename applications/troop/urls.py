from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('troop.views',
    url(r'^$', 'troopHome', name='troop_home'),
    url(r'^home/', 'troopHome', name='troop_home'),
    url(r'^new/', 'NewTroop', name='new_troop'),
    url(r'^overview/', 'troopOverview', name='troop_overview'),
    #url(r'^calendar/', direct_to_template, {'template':'troop/calendar.html'}),
    url(r'^calendar/', TemplateView.as_view(template_name='troop/calendar.html'), name="calendar"),
    )