

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from utils.decorators import render_to_html, login_required
from utils.google_funcs import get_token_from_code, get_google_profile


from userprofile.forms import NewScoutForm
from userprofile.views import userhome

"""
/*
{u'family_name': u'Carter', u'name': u'Enoch Carter', u'picture': 
    u'https://lh6.googleusercontent.com/-OY6QProkKnI/AAAAAAAAAAI/AAAAAAAAAgU/d3n117polaY/photo.jpg', 
    u'locale': u'en-US', u'gender': u'male', u'email': u'mrenoch@gmail.com', 
    u'link': u'https://plus.google.com/109887084995893744580', u'given_name': u'Enoch', 
    u'id': u'109887084995893744580', u'verified_email': True}
*/
"""

@render_to_html
def anon_home(request):
    try:
        if request.user.is_authenticated():
            return userhome(request, request.user.pk)
        return 'home.html', {}
    except:
        logout(request)
        #request.user.logout()
        return HttpResponseRedirect("/") 
    


@render_to_html
def oauth_callback(request):
    if request.method == 'GET':
        code = request.GET.get('code',None)
        if 'google_access_token' in request.session:
            del request.session['google_access_token']
    
        if code is not None:
            request.session['google_oauth_code'] = code
            data =  get_token_from_code(code)
            request.session['google_access_token'] = data['access_token']
            user = authenticate(token=request.session['google_access_token'])
            if user is None:
                profile = get_google_profile(request.session['google_access_token'])
                print profile

                form = NewScoutForm(initial={'first_name':profile["given_name"],
                                             'last_name':profile["family_name"],
                                             'nickname':profile["given_name"],
                                             'login_name':profile["email"],
                                             'email':profile["email"],
                                             'google_id':profile["id"],
                                             'position':7,
                                             })
                return 'oauth.html', {'form':form, 'profile':True}
            else:
                login(request, user)
                return HttpResponseRedirect("/user")
        else:
            form = NewScoutForm(initial={
                                         'position':7,#Guardian
                                         })
            return 'oauth.html', {'form':form}  
        
    elif request.method == 'POST':

        scoutform = NewScoutForm(request.POST)
       
        if scoutform.is_valid():
            profile = scoutform.save()
            if len(profile.google_id) > 0:
                user = authenticate(token=request.session['google_access_token'], google_id=profile.google_id)
                print 'auth1, %s'%user
            else:
                print 'password: %s, %s'%(scoutform.cleaned_data['password'],profile.user.username)
                user = authenticate(username=profile.user.username, password=scoutform.cleaned_data['password'])
                print 'auth2, %s'%user
            if user:
                login(request, user)
            return HttpResponseRedirect("/")
        else:
            print 'form errors: %s'%scoutform.errors
            return 'oauth.html', {'form':scoutform}
        
        
        
    
    

    