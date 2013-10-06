from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from utils.decorators import render_to_html, login_required
from utils.response import HttpJsonSuccess, HttpJsonFailure, HttpJsonFormError

from applications.award.models import Award


def award_list(request):
    awards = Award.objects.all().order_by("name")
    return HttpJsonSuccess({"list":[b.name for b in awards]})