import os

from amsp import settings

from django.core.wsgi import get_wsgi_application

os.environ.update(DJANGO_SETTINGS_MODULE='amsp.settings')

application = get_wsgi_application()

