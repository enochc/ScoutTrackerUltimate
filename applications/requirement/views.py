import datetime

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import date as _date

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
            return HttpJsonFailure(str(e))

        if request.user.has_perm('userprofile.mark_requirements') or request.user.profile == profile:
            try:
                ur = UserRequirement.objects.get(user=profile.user, requirement=req)
            except UserRequirement.DoesNotExist:
                ur = UserRequirement(user=profile.user, requirement=req, signed_by=request.user)

            completed = request.POST.get('completed') in (True, 'true', 'True', 1)
            
            if completed:
                try:
                    ur.completed_date = datetime.datetime.strptime(request.POST.get('date'), '%b %d, %Y')
                except Exception, e:
                    ur.completed_date = datetime.datetime.now()
            else:
                ur.completed_date = None
            ur.completed = completed
            ur.signed_by = request.user

            notes = request.POST.get('notes',None)
            if notes == '':
                notes = None
            notes = notes
            ur.notes = notes
            ur.save()
            
            return HttpJsonSuccess({'completed':completed, 'notes':notes, 'date':_date(ur.completed_date)})
        else:
            return HttpJsonFailure('You are not authorized to perform this action')

@render_to_html
def req_info(request, req_id):
    req = Requirement.objects.get(pk=req_id)
    return 'requirement/info.html', {'req':req }


@render_to_html
@login_required
def rank_requirements(request, rank_id):
    rank = Rank.objects.get(pk=rank_id)
    unit = request.user.profile.unit
    patrols = unit.patrol_set.all()
    member_list = {}
    if unit is not None:
        for p in patrols:
            for m in p.patrol_members.all():
                member_list[m.pk] = m.completed_list(rank)
    else:
        member_list[request.user.profile.pk] = request.user.profile.completed_list(rank)
    
    return 'requirement/by_rank.html', {'rank':rank, 'unit':unit, 'member_list':member_list, 'patrols':patrols}
