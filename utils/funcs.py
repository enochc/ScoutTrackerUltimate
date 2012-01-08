from sorl.thumbnail import get_thumbnail, delete
from django.conf import settings

def get_sized_image(img, size_tuple=None):

    if size_tuple is not None and isinstance(size_tuple, tuple):
        return get_thumbnail(str(img),"%sx%s"%(size_tuple))
        
    else:
        return img
    
def baseProcessor(httprequest):
    return {'google_client_id':settings.GOOGLE_CLIENT_ID,
            }