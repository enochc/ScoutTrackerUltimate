from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from utils.decorators import render_to_html, login_required
from utils.response import HttpJsonSuccess, HttpJsonFailure

from requirement.models import Requirement
from userprofile.models import Userprofile
from userrequirement.models import UserRequirement
from rank.models import Rank

@render_to_html
@login_required
def req_set(request, req_id, user_id):
    try:
        req = Requirement.objects.get(pk=req_id)
        profile = Userprofile.objects.get(pk=user_id)
    except Exception, e:
        return HttpJsonFailure(sttr(e))
    
    if request.user.has_perm('userprofile.signoff') or request.user.profile == profile:
    
        ur = UserRequirement(user=profile.user, requirement=req, completed=True, signed_by=request.user)
        ur.save()
        
        return HttpJsonSuccess()
    else:
        return HttpJsonFailure('You are not authorized to perform this action')

@render_to_html
def req_info(request, req_id):
    req = Requirement.objects.get(pk=req_id)
    return 'requirement/info.html', {'req':req }


@render_to_html
def rank_requirements(request, rank_id):
    rank = Rank.objects.get(pk=rank_id)
    troop = request.user.profile.troop
    member_list = {}
    for m in troop.members.all():
        member_list[m.pk] = m.completed_list(rank)
    return 'requirement/by_rank.html', {'rank':rank, 'troop':troop, 'member_list':member_list}