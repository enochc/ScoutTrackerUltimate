from django import template

register = template.Library()

@register.inclusion_tag('email_macros/t1.html')
def t1(text=None):
    return {'text':text}      
   
@register.tag()
def span1 (parser,token):
    nodelist = parser.parse(('endspan1',))
    parser.delete_first_token()
    return span1func(nodelist)

class span1func(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        output = self.nodelist.render(context)
        return "<span style=\"font-size:8pt;\
        color:#00525E;font-family:universe,myriad pro,ariel;\">%s</span>"%output