
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from utils.decorators import render_to_html, login_required
from utils.response import HttpJsonSuccess, HttpJsonFailure, HttpJsonFormError

from userprofile.forms import NewScoutForm
from userprofile.models import Userprofile
from position.models import Position
from userrequirement.models import UserRequirement
from rank.models import Rank
from award.models import Award
from unit.models import Patrol


@render_to_html
@login_required
def userhome(request, user_id=None):
    user = request.user
    scout = None
    req_list = {}
    ranks = {}
    urs = {}
    patrols = []
    orphans = []


    if user_id is not None and request.user.has_perm('userprofile.add_scouts'):
        scout = get_object_or_404(User, id=user_id, profile__unit=user.profile.unit)
    else:   
        scout = user  
    
    if scout.profile.position.youth:
        urs = UserRequirement.objects.filter(user=scout)
        req_list = scout.profile.completed_list()  
        ranks = Rank.objects.all()
    elif scout.profile.unit:
        patrols = scout.profile.unit.patrol_set.all()
        orphans = Userprofile.objects.filter(patrol=None, unit=scout.profile.unit, position__youth=True)
        
    awards = Award.objects.all()
        
    return 'userprofile/user_home.html', {'scout':scout.profile, 
                                          'userrequirements':urs, 
                                          'req_list':req_list,
                                          'ranks':ranks,'badges':awards,
                                          'patrols':patrols,
                                          'orphans':orphans}

@render_to_html
def add_scout(request, scout_id = None):  
    if request.method == 'GET':
        edit = int(request.GET.get('edit','0')) == 1
        boyscout = Position.objects.get(name='Boy Scout')
        scout = None
        unit = None
        try:
            unit = request.user.profile.unit
        except:
            pass
        
        patrol = request.REQUEST.get('patrol')
        if patrol and unit:
            try:
                patrol = Patrol.objects.get(name=patrol, unit=unit)
            except Patrol.DoesNotExist:
                pass
        

        if scout_id is not None:
            scout = Userprofile.objects.get(pk=scout_id)
            form = NewScoutForm(instance=scout, initial={"first_name":scout.user.first_name,
                                                         "last_name":scout.user.last_name,
                                                         "email":scout.user.email})
        else:
            form = NewScoutForm(initial={'email':'noemail', 'unit':unit, 'patrol':patrol})
        
            
        return 'userprofile/add_scout.html', {'form':form, 'boyscout':boyscout, 'scout':scout, 'edit':edit}
    
    else:
        try:
            scout = NewScoutForm(request.POST)
            if request.POST.get('scout_id',False):
                scoutid = request.POST.get('scout_id')
                scout = Userprofile.objects.get(pk=scoutid)
                scoutform = NewScoutForm(request.POST, instance=scout)
            else:
                scoutform = NewScoutForm(request.POST)
        except Exception,e:
            print 'error', e
            
        try:    
            if scoutform.is_valid():
                scoutform.save()
            else:
                return HttpJsonFormError(scoutform.errors)
            return HttpJsonSuccess()
        except Exception, e:
            print e
        