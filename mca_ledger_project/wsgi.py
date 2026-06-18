# WSGI placeholder
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mca_ledger_project.settings')

application = get_wsgi_application()