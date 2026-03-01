"""WSGI config for ecompro project."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecompro.config.settings')

application = get_wsgi_application()
