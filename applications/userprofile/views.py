
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from utils.decorators import render_to_html, login_required
from utils.response import HttpJsonSuccess, HttpJsonFailure, HttpJsonFormError

from userprofile.forms import NewScoutForm
from position.models import Position
from requirement.models import Requirement

@permission_required('polls.can_vote')


@render_to_html
@login_required
def userhome(request, user_id=None):
    user = request.user
    scout = None
    requirements = None
    req_list = {}
    requirements = Requirement.objects.all()
    scout_position = Position.objects.get(name='Boy Scout')
    if user_id is not None and request.user.has_perm('userprofile.add_scouts'):
        scout = get_object_or_404(User, id=user_id, profile__troop=user.profile.troop)
    else:   
        scout = user  
    
    if scout.profile.position.youth:
        requirements = Requirement.objects.all()
        req_list = scout.profile.completed_list()  
        
    return 'userprofile/user_home.html', {'scout':scout.profile, 
                                          'requirements':requirements, 
                                          'req_list':req_list,
                                          'scout_patch':scout_position.patch}

@render_to_html
@permission_required('userprofile.add_scout')
def add_scout(request):  
    if request.method == 'GET':
        boyscout = Position.objects.get(name='Boy Scout')
        form = NewScoutForm()
        return 'userprofile/add_scout.html', {'form':form, 'boyscout':boyscout}
    
    else:
        scout = NewScoutForm(request.POST)
        if scout.is_valid():
            scout.save()
        else:
            return HttpJsonFormError(scout.errors)
        return HttpJsonSuccess()
        