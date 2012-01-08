from utils.decorators import render_to_html, login_required
from django.http import HttpResponse
from utils.google_funcs import get_token_from_code, get_google_profile

@render_to_html
def oauth_callback(request):
    code = request.GET.get('code',None)
    print 'code: %s'%code
    if code is not None:
        data =  get_token_from_code(code)
        profile = get_google_profile(data['access_token'])
        return 'oauth.html', {'profile':profile}
    else:
        return HttpResponse("no code")
        

    