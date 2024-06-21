from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PPM.settings')

application = get_wsgi_application()


app = application
