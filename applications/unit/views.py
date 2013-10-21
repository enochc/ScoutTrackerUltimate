import hashlib

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

from utils.decorators import render_to_html, login_required
from utils.response import HttpJsonSuccess, HttpJsonFailure, HttpJsonFormError
from requirement.models import Requirement
from rank.models import Rank
from unit.forms import UnitForm, UnitRequestForm
from unit.models import Patrol
from position.models import Position
from userprofile.models import Userprofile

from userprofile.views import userhome
from models import UnitRequest

@render_to_html
@login_required
def unitHome(request):
    return 'unit/unit_home.html'


@login_required
def unitRequest(request):
    if request.method == "GET":
        return HttpResponseRedirect("/")
    elif request.method == "POST":
        form = UnitRequestForm(request.POST, scout=request.user)
        if form.is_valid():
            req = form.save()
            req.notify()
        else:
            return userhome(request, request_form=form)
        return userhome(request)

@login_required
def unitInvite(request):
    email = request.REQUEST.get('email')
    if email:
        form = UnitRequestForm({'member':request.user.profile.id,
                                'email':email,
                                'type':'invite',
                                'unit':request.user.profile.unit.id})
        if form.is_valid():
            req = form.save()
            req.notify()
        else:
            return HttpJsonFailure("Doh! failed")
        return HttpJsonSuccess()
    
@render_to_html
def acceptInvite(request, key):
    req = UnitRequest.objects.get(key=key)
    if req:
        if request.user.is_authenticated():
            req.claim(request.user)
            return HttpResponseRedirect("/")
        else:
            request.session['req'] = req
    else:
        del request.session['req']
    return 'home.html',{}

@login_required
def cancelUnitRequest(request, req_id):
    try:
        req = UnitRequest.objects.get(pk=req_id)
        req.delete()
        return HttpJsonSuccess()
    except UnitRequest.DoesNotExist:
        return HttpJsonFailure("Request specified does not exist")
    
@login_required
def approveUnitRequest(request, req_id):
    try:
        req = UnitRequest.objects.get(pk=req_id)
        req.approve(request.user)
        return HttpJsonSuccess()
    except UnitRequest.DoesNotExist:
        return HttpJsonFailure("Request specified does not exist")
    

@login_required
def addToPatrol(request):
    scout_id = request.REQUEST.get("scout")
    patrol_id = request.REQUEST.get("patrol")
    if scout_id and patrol_id:
        scout = Userprofile.objects.get(pk=scout_id)
        scout.patrol = Patrol.objects.get(pk=patrol_id)
        scout.save()
        return HttpJsonSuccess()
    else:
        
        return HttpJsonFailure("patrol or scout does not exist")
    
@login_required
def delPatrol(request, patrol_id):

    patrol = Patrol.objects.get(pk=patrol_id)
    patrol.delete()
    return HttpJsonSuccess()

@login_required
def delLeader(request, leader_id):
    user = Userprofile.objects.get(pk=leader_id)
    user.unit = None
    user.position = Position.objects.get(name="Guardian")
    user.save()
    return HttpJsonSuccess()

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
        patrol.save()
        return HttpJsonSuccess()

@login_required
def updateCalendar(request):
    unit = request.user.profile.unit
    cal_id = request.REQUEST.get("calendar_id")
    unit.calendar = cal_id
    unit.save()
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
    patrols = Patrol.objects.filter(unit=unit)
    
    return 'unit/overview.html', {
                                   'ranks':ranks,
                                   'unit':unit,
                                   'patrols':patrols 
                                   #'requirements':requirements, 
                                   #'member_list':member_list
                                   }
