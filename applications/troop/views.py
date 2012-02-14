from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from utils.decorators import render_to_html, login_required
from utils.response import HttpJsonSuccess, HttpJsonFailure, HttpJsonFormError
from requirement.models import Requirement
from rank.models import Rank
from troop.forms import TroopForm
from position.models import Position

@render_to_html
@login_required
def troopHome(request):
    return 'troop/troop_home.html'


@render_to_html
@login_required
def NewTroop(request):
    if request.method == "GET":
        form = TroopForm()
        roles = Position.objects.filter(youth=False).exclude(id=7) # Guardian
        
        #send_mail('Subject', 'Here is the message.', 'notify@ultimatescouttracker.com',
        #['mrenoch@gmail.com'], fail_silently=False)
        
        return 'troop/new_troop.html', {'form':form, 'roles':roles}
    else:
        troopform = TroopForm(request.POST)
        
        if troopform.is_valid():
            troop = troopform.save()
            request.user.profile.troop = troop
            pos = Position.objects.get(pk=troopform.cleaned_data['user_role'])
            request.user.profile.position = pos;
            request.user.profile.save()
            
            return HttpJsonSuccess()
        else:
            return HttpJsonFormError(troopform.errors)
       

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
