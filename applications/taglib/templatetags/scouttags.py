from django import template
from django.template.defaultfilters import stringfilter

from userrequirement.models import UserRequirement


register = template.Library()

@register.filter("attribute")
def attribute( value,arg ):
    try:
        val = get_attribute(value, arg)
        if val is None:
            val = get_attribute(value, str(arg))
    except:
        try:
            val = value[arg]
            if val is None:
                val = value[str(arg)]
            return val
        except:
            pass
        return None  
    
@register.simple_tag(takes_context=True)
def user_requirement(context):
    user = context['user']
    list = context['userrequirements']
    req = context['req']
    
    #  newlist = [s for s in a_list if not any(r(s) for r in regex_list)]
    try:
        ur = [u for u in list if u.requirement == req]
        context['user_requirement'] = ur[0]
    except Exception,e:
        context['user_requirement'] = None
    
    return ''

