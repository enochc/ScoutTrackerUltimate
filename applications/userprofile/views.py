from utils.decorators import render_to_html, login_required

@render_to_html
@login_required
def userhome(request):
    return 'userprofile/user_home.html'