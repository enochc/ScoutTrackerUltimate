
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from utils.decorators import render_to_html, login_required

from userprofile.forms import NewScoutForm

@permission_required('polls.can_vote')


@render_to_html
@login_required
def userhome(request):
    return 'userprofile/user_home.html'

@render_to_html
@permission_required('userprofile.add_scout')
def add_scout(request):
    
    
    if request.method == 'GET':
        form = NewScoutForm()
        return 'userprofile/add_scout.html', {'form':form}
    
    else:
        scout = NewScoutForm(request.POST)
        if scout.is_valid():
            scout.save()
        return 'userprofile/add_scout.html', {'form':scout}
        