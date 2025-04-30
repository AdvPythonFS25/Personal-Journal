
import os
#Connects app to web server WSGI(Web Server Gateway Interface).
#also manages which settings to use
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal_project.settings')

application = get_wsgi_application()
