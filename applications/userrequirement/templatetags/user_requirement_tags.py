from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def has_requirement(value, args):
    user, req = args.split(' ')
    print user, req
    return False