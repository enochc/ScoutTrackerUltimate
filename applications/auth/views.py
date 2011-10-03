from django.contrib.auth import logout, authenticate, login
from django.utils.translation import ugettext as _

from applications.userprofile.models import Userprofile


from utils.response import HttpJsonResponse, HttpJsonSuccess, HttpJsonFailure

def login_view(request):
    username = request.POST['login']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            profile = Userprofile.objects.get_or_create(user=user)
            return HttpJsonSuccess()
        else:
            return HttpJsonFailure(_("The provided accout is not yet active."))
    else:
        return HttpJsonFailure(_("Invalid email or password"))
    

def logout_view(request):
    logout(request)
    return HttpJsonSuccess()