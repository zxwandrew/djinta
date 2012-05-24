import os
import sys
 
path = '/srv/www/djinta'
if path not in sys.path:
    sys.path.insert(0, '/srv/www/djinta')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'djinta.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp/pythoneggs'

 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

