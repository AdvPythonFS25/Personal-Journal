import os
#Handles web requests
from django.core.asgi import get_asgi_application
#Sets up settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_project.settings')

application = get_asgi_application()
