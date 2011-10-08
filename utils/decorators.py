from django.template import RequestContext,Context, loader
from django.http import HttpResponse, HttpResponseRedirect

def _render_html(request, template, args):
    t = loader.get_template(template)
    c = RequestContext(request, args)
    return HttpResponse(t.render(c))


def login_required(f):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
        
        
    return inner

def render_to_html(func):
    def innerf(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        
        if isinstance(response, HttpResponse):
            return response
        
        elif isinstance(response, basestring):
            template_name = response
            context_processors = {}
        elif isinstance(response, (tuple, list)):
            len_tuple = len(response)
            if len_tuple == 2:
                template_name, context_processors = response
            elif len_tuple == 3:
                template_name, context_processors, mimetype = response
        else:
            print response
        return _render_html(request, template_name, context_processors)

    return innerf