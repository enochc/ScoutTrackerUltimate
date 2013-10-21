from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('unit.views',
    url(r'^$', 'unitHome', name='unit_home'),
    url(r'^home/', 'unitHome', name='unit_home'),
    url(r'^invite/cancel/(?P<req_id>\d+)/', 'cancelUnitRequest', name='cancel_unit_request'),
    url(r'^invite/approve/(?P<req_id>\d+)/', 'approveUnitRequest', name='approve_unit_request'),
    url(r'^invite/accept/(?P<key>.+)/', 'acceptInvite', name='accept_invite'),
    url(r'^invite/', 'unitInvite', name='unit_invite'),
    url(r'^request/', 'unitRequest', name='unit_request'),
    url(r'^del_patrol/(?P<patrol_id>\d+)/', 'delPatrol', name='del_patrol'),
    url(r'^del_leader/(?P<leader_id>\d+)/', 'delLeader', name='del_leader'),
    
    
    url(r'^new/', 'newUnit', name='new_unit'),
    url(r'^newpatrol/', 'newPatrol', name='new_patrol'),
    url(r'^add/', 'addToPatrol', name='add_to_patrol'),
    url(r'^overview/', 'unitOverview', name='unit_overview'),
    #url(r'^calendar/', direct_to_template, {'template':'unit/calendar.html'}),
    url(r'^update_calendar/', 'updateCalendar', name="update_calendar"),
    url(r'^calendar/', TemplateView.as_view(template_name='unit/calendar.html'), name="calendar"),
    )