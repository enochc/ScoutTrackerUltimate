
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from utils.decorators import render_to_html, login_required

from userprofile.forms import NewScoutForm
from position.models import Position

@permission_required('polls.can_vote')


@render_to_html
@login_required
def userhome(request, user_id=None):
    user = request.user
    scout = None
    if user_id is not None and request.user.has_perm('userprofile.add_scouts'):
        scout = get_object_or_404(User, pk=user_id, profile__troop=user.profile.troop)
    else:   
        scout == user    
        
    return 'userprofile/user_home.html', {'scout':scout}

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
        return 'userprofile/add_scout.html', {'form':scout}
        