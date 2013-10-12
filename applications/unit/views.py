from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from utils.decorators import render_to_html, login_required
from utils.response import HttpJsonSuccess, HttpJsonFailure, HttpJsonFormError
from requirement.models import Requirement
from rank.models import Rank
from unit.forms import UnitForm
from unit.models import Patrol
from position.models import Position

@render_to_html
@login_required
def unitHome(request):
    return 'unit/unit_home.html'

@render_to_html
@login_required
def newPatrol(request):
    pname = request.REQUEST.get("pname")
    scout = request.user.profile
    unit = scout.unit
    try:
        patrol = Patrol.objects.get(unit=unit,name=pname)
        return HttpJsonFailure("Patrol %s already exists"%pname)
    except:
        patrol = Patrol.objects.create(name=pname,unit=unit)
        scout.add_patrol(patrol)
        return HttpJsonSuccess()
    
    

@render_to_html
@login_required
def newUnit(request):
    if request.method == "GET":
        form = UnitForm()
        roles = Position.objects.filter(youth=False).exclude(id=7) # Guardian
        
        #send_mail('Subject', 'Here is the message.', 'notify@ultimatescouttracker.com',
        #['mrenoch@gmail.com'], fail_silently=False)
        
        return 'unit/new_unit.html', {'form':form, 'roles':roles}
    else:
        unitform = UnitForm(request.POST)
        
        if unitform.is_valid():
            unit = unitform.save()
            request.user.profile.unit = unit
            pos = Position.objects.get(pk=unitform.cleaned_data['user_role'])
            request.user.profile.position = pos;
            request.user.profile.save()
            
            return HttpJsonSuccess()
        else:
            return HttpJsonFormError(unitform.errors)
       

@render_to_html
@login_required
def unitOverview(request):
    unit = request.user.profile.unit
    #requirements = Requirement.objects.all()
    #member_list = {}
    #for m in unit.members.all():
    #    member_list[m.pk] = m.completed_list()
        
    ranks = Rank.objects.all()
    
    return 'unit/overview.html', {
                                   'ranks':ranks,
                                   'unit':unit, 
                                   #'requirements':requirements, 
                                   #'member_list':member_list
                                   }
