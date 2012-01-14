from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from utils.decorators import render_to_html, login_required
from requirement.models import Requirement
from rank.models import Rank
from troop.forms import TroopForm

@render_to_html
@login_required
def troopHome(request):
    return 'troop/troop_home.html'


@render_to_html
@login_required
def NewTroop(request):
    if request.method == "GET":
        form = TroopForm()
        return 'troop/new_troop.html', {'form':form}
    else:
        pass
        return HttpResponse('troop form, not get')

@render_to_html
@login_required
def troopOverview(request):
    troop = request.user.profile.troop
    #requirements = Requirement.objects.all()
    #member_list = {}
    #for m in troop.members.all():
    #    member_list[m.pk] = m.completed_list()
        
    ranks = Rank.objects.all()
    
    return 'troop/overview.html', {
                                   'ranks':ranks,
                                   'troop':troop, 
                                   #'requirements':requirements, 
                                   #'member_list':member_list
                                   }
