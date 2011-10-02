from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from utils.decorators import render_to_html, login_required

@render_to_html
@login_required
def troopHome(request):
    return 'troop/troop_home.html'