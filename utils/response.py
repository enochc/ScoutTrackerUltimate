import simplejson as json
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, \
    HttpResponseForbidden, HttpResponseBadRequest

def json_vals(vals, mimetype):
    if settings.DEBUG:
        return HttpResponse( json.dumps( vals, indent=2 ), mimetype )
    else:
        return HttpResponse( json.dumps( vals, seperators=(',',':') ), mimetype)

def HttpJsonResponse(vals, mimetype="application/json"):
    return json_vals(vals, mimetype)

def HttpJsonSuccess(params = None, mimetype="application/json"):
    values = { 'success' : True }
    if params:
        values.update(params)
    return json_vals(values, mimetype)

def HttpJsonBadPost():
    return HttpJsonFailure('Invalid post data.')

def HttpJson404():
    return HttpJsonFailure('Object not found.')

def HttpJsonLoginRequired():
    return HttpJsonFailure('User must login.', { 'authenticated' : False })

def HttpJsonFormError(errors, message='Form invalid.', mimetype="application/json"):
    # TODO: This is unpleasant and would be better served by adding a handler
    # to the JSON serializer. It is nececsary because Django wraps values in 
    # a proxy object which does not directly serialize.
    myd = errors.items()
    return HttpJsonFailure(message, myd, mimetype)

def HttpJsonFailure(message, params=None, mimetype="application/json"):
    values = { 'success': False, 'message': message } 
    if params:
        values.update(params)

    return json_vals(values, mimetype)
