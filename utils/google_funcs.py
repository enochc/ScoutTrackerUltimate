from django.conf import settings
import urllib
import urllib2
import json

def get_token_from_code(code):
    url = "https://accounts.google.com/o/oauth2/token"
    values = {"scope":"https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
            "code":code,
            "redirect_uri":"http://ultimatescouttracker.com/oauth2callback",
            "client_secret":settings.GOOGLE_CLIENT_SECRET,
            "client_id":settings.GOOGLE_CLIENT_ID,
            "grant_type":"authorization_code"
            }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    data = json.loads(the_page)

    return data

def get_google_profile(token):
    url = "https://www.googleapis.com/oauth2/v1/userinfo?access_token=%s"%token
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()

    data = json.loads(the_page)
    return data