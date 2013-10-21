from django.contrib.auth import logout, authenticate, login
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout


from applications.userprofile.models import Userprofile
from applications.userprofile.forms import NewScoutForm

from utils.response import HttpJsonSuccess, HttpJsonFailure, HttpJsonFormError
from utils.decorators import render_to_html, login_required
from utils.response import HttpJsonResponse, HttpJsonSuccess, HttpJsonFailure
from utils.funcs import USTLogin

@render_to_html
def login_view(request):
    username = request.POST['login']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            profile, created = Userprofile.objects.get_or_create(user=user)
            return HttpResponseRedirect("/")
        else:
            #return HttpJsonFailure(_("The provided account is not yet active."))
            return "home.html", {"login_error": _("The provided account is not yet active.")}
    else:
        #return HttpJsonFailure(_("Invalid login or password"))
        return "home.html", {"login_error": _("Invalid login or password.")}
    

def fblogin_view(request):
    print request.POST
    fb_id = request.POST.get("userID")
    email = request.POST.get("email")
    if email:
        fb_id = request.POST.get("id")
        # create new use, then authticate them
        try:
            user = User.objects.get(email=email)
        
       
            if user.profile.facebook_id and user.profile.facebook_id != fb_id:
                return HttpJsonFailure("This email address is already associated with another facebook id")
            user.profile.facebook_id = request.POST.get("id")
            user.profile.save()
            user = USTLogin(request, username=user.username, facebook_id=fb_id)
            
            if not user:
                return HttpJsonFailure("something wrogn")
            
            return HttpJsonSuccess()
        except User.DoesNotExist:
            #build new user
            form = NewScoutForm({'first_name':request.REQUEST.get("first_name"),
                                     'last_name':request.REQUEST.get("last_name"),
                                     'nickname':request.REQUEST.get("name"),
                                     'login_name':request.REQUEST.get("email"),
                                     'bd_string':request.REQUEST.get("birthday",''),
                                     'email':request.REQUEST.get("email"),
                                     'facebook_id':fb_id,
                                     'position':7,
                                     })
            if form.is_valid():
                profile = form.save()
                user = USTLogin(request, username=profile.user.username, facebook_id=fb_id)
                if user:
                    return HttpJsonSuccess()
            
            return HttpJsonFailure("not implimented")
        
        
    elif fb_id:
        #login user
        try:
            user = User.objects.get(profile__facebook_id=fb_id)
            user = USTLogin(request, username=user.username, facebook_id=fb_id)
            
            if not user:
                return HttpJsonFailure("something wrong 2")

            return HttpJsonSuccess()
        except User.DoesNotExist:
            return HttpJsonFailure("no user")
    else:
        return HttpJsonFailure("no facebook id")

    

def logout_view(request):
    logout(request)
    return HttpJsonSuccess()

