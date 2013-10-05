from django.contrib.auth import logout, authenticate, login
from django.utils.translation import ugettext as _

from applications.userprofile.models import Userprofile


from utils.response import HttpJsonResponse, HttpJsonSuccess, HttpJsonFailure

def login_view(request):
    username = request.POST['login']
    password = request.POST['password']
    print 'authenticate: %s, %s'%(username, password)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            profile, created = Userprofile.objects.get_or_create(user=user)
            return HttpJsonSuccess()
        else:
            return HttpJsonFailure(_("The provided account is not yet active."))
    else:
        return HttpJsonFailure(_("Invalid login or password"))
    

def logout_view(request):
    logout(request)
    return HttpJsonSuccess()
