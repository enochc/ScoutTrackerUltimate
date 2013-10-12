from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('unit.views',
    url(r'^$', 'unitHome', name='unit_home'),
    url(r'^home/', 'unitHome', name='unit_home'),
    url(r'^new/', 'newUnit', name='new_unit'),
    url(r'^newpatrol/', 'newPatrol', name='new_patrol'),
    url(r'^overview/', 'unitOverview', name='unit_overview'),
    #url(r'^calendar/', direct_to_template, {'template':'unit/calendar.html'}),
    url(r'^calendar/', TemplateView.as_view(template_name='unit/calendar.html'), name="calendar"),
    )