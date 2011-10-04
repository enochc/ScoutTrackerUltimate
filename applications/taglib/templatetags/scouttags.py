from django import template
from django.template.defaultfilters import stringfilter

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
        return ''  