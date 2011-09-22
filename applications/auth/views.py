from django.contrib.auth import logout

from utils.response import HttpJsonResponse, HttpJsonSuccess

def login(request):
    return HttpJsonSuccess()

def logout_view(request):
    logout(request)
    return HttpJsonSuccess()