"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
from waitress import serve
import sys

# Add the project root directory to the sys.path (only needed if necessary)
sys.path.append(os.path.join(os.path.dirname(__file__), 'farm_marketplace'))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Get the WSGI application
application = get_wsgi_application()