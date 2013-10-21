import os
import sys

path = '/home/enoch/work/'
if path not in sys.path:
    sys.path.append(path)

os.environ['PYTHON_EGG_CACHE'] = '/home/enoch/.python-eggs'
os.environ['DJANGO_SETTINGS_MODULE'] = 'scouts.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()