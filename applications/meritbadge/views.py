from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from utils.decorators import render_to_html, login_required
from utils.response import HttpJsonSuccess, HttpJsonFailure, HttpJsonFormError

from applications.meritbadge.models import Badge


def badge_list(request):
    badges = Badge.objects.all().order_by("name")
    return HttpJsonSuccess({"list":[b.name for b in badges]})