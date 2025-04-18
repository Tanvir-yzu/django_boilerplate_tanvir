

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_boilerplate_tanvir.settings')

application = get_wsgi_application()
