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
def req_set(request, req_id, user_id, completed = True):
    if request.method == 'GET':
         
        req = Requirement.objects.get(pk=req_id)
        profile = Userprofile.objects.get(pk=user_id)
        ur = None
        try:
            ur = UserRequirement.objects.get(user=profile.user, requirement=req)
        except UserRequirement.DoesNotExist:
            pass
              
        return 'requirement/set_requirement.html', {'req': req, 'scout': profile, 'ur':ur}
        
    elif request.method == 'POST':
        try:
            req = Requirement.objects.get(pk=req_id)
            profile = Userprofile.objects.get(pk=user_id)
        except Exception, e:
            return HttpJsonFailure(sttr(e))
        
        if request.POST.get('action', 'add') == 'remove':
            try:
                 ur = UserRequirement.objects.filter(user=profile.user, requirement=req)
                 ur.delete()
            except UserRequirement.DoesNotExist:
                pass
            return HttpJsonSuccess({'removed':True})
        else:
        
            if request.user.has_perm('userprofile.signoff') or request.user.profile == profile:
                try:
                    ur = UserRequirement.objects.get(user=profile.user, requirement=req)
                except UserRequirement.DoesNotExist:
                    ur = UserRequirement(user=profile.user, requirement=req)
                ur.completed = completed
                ur.signed_by = request.user
                notes = request.POST.get('notes',None)
                ur.notes = notes
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