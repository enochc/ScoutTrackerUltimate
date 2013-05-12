import datetime
from sorl.thumbnail import get_thumbnail, delete
from django.conf import settings
from utils.google_funcs import get_google_profile, validate_token

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


def get_sized_image(img, size_tuple=None):

    if size_tuple is not None and isinstance(size_tuple, tuple):
        return get_thumbnail(str(img),"%sx%s"%(size_tuple))
        
    else:
        return img
    
def baseProcessor(httprequest):
    return {
            #'host':'%s:%s'%(httprequest.META.get('REMOTE_ADDR'),httprequest.META.get('SERVER_PORT')),
            'google_client_id':settings.GOOGLE_CLIENT_ID,
            }

def add_months(months, date):
    m=0
    month = date.month
    day = date.day
    mod = -1 if months<0 else 1
    while m < abs(months):
        date = date+datetime.timedelta(days=mod)
        if month != date.month:
            m+=1
            month = date.month
    
    while date.day != day:
        date = date+datetime.timedelta(days=mod)          
    return date

class CaseInsensitiveBackend(ModelBackend):
    """
    Authenticates against django.contrib.auth.models.User.
    """
    supports_object_permissions = False
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username__iexact=username, is_active=True)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None   

   
class GoogleOauthModelBackend(ModelBackend):
    #supports_object_permissions = False
    #supports_anonymous_user = True
    supports_inactive_user = True
    
    def authenticate(self, token=None, google_id=None):
        try:
            if google_id is not None and validate_token(token, google_id):
                return User.objects.get(profile__google_id=google_id)
            profile = get_google_profile(token)
            google_id = profile['id']
            return User.objects.get(profile__google_id=google_id)
        except User.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm):
        return perm in self.get_all_permissions(user_obj)