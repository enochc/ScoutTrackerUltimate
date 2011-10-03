from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from utils.decorators import render_to_html, login_required
from requirement.models import Requirement

@render_to_html
@login_required
def troopHome(request):
    return 'troop/troop_home.html'


@render_to_html
@login_required
def troopOverview(request):
    troop = request.user.profile.troop
    requirements = Requirement.objects.all()
    member_list = {}
    for m in troop.members.all():
        member_list[m.id] = m.completed_list
    
    return 'troop/overview.html', {'troop':troop, 'requirements':requirements, 'member_list':member_list}