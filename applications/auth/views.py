from django.contrib.auth import logout, authenticate, login
from django.utils.translation import ugettext as _

from applications.userprofile.models import UserProfile


from utils.response import HttpJsonResponse, HttpJsonSuccess, HttpJsonFailure

def login_view(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            profile = UserProfile.objects.get_or_create(user=user)
            return HttpJsonSuccess()
        else:
            return HttpJsonFailure(_("The provided accout is not yet active."))
    else:
        return HttpJsonFailure(_("Invalid email or password"))
    

def logout_view(request):
    logout(request)
    return HttpJsonSuccess()