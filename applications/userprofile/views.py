
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


@render_to_html
@login_required
def userhome(request, user_id=None):
    user = request.user
    scout = None
    req_list = {}
    ranks = {}
    urs = {}
    


    if user_id is not None and request.user.has_perm('userprofile.add_scouts'):
        scout = get_object_or_404(User, id=user_id, profile__troop=user.profile.troop)
    else:   
        scout = user  
    
    if scout.profile.position.youth:
        urs = UserRequirement.objects.filter(user=scout)
        req_list = scout.profile.completed_list()  
        ranks = Rank.objects.all()
        
        
    return 'userprofile/user_home.html', {'scout':scout.profile, 
                                          'userrequirements':urs, 
                                          'req_list':req_list,
                                          'ranks':ranks}

@render_to_html
@permission_required('userprofile.add_scout')
def add_scout(request, scout_id = None):  
    if request.method == 'GET':
        edit = int(request.GET.get('edit','0')) == 1
        boyscout = Position.objects.get(name='Boy Scout')
        scout = None
        if scout_id is not None:
            scout = Userprofile.objects.get(pk=scout_id)
            form = NewScoutForm(instance=scout, initial={'first_name':scout.user.first_name,
                                                         'last_name':scout.user.last_name,
                                                         'login_name':scout.user.username.split("_")[0]})
        else:
            form = NewScoutForm()
        return 'userprofile/add_scout.html', {'form':form, 'boyscout':boyscout, 'scout':scout, 'edit':edit}
    
    else:
        scout = NewScoutForm(request.POST)
        if request.POST.get('scout_id',False):
            scoutid = request.POST.get('scout_id')
            scout = Userprofile.objects.get(pk=scoutid)
            scoutform = NewScoutForm(request.POST, instance=scout)
        else:
            scoutform = NewScoutForm(request.POST)
        try:    
            if scoutform.is_valid():
                scoutform.save()
            else:
                return HttpJsonFormError(scoutform.errors)
            return HttpJsonSuccess()
        except Exception, e:
            print e
        