import os
import django
from django.conf import settings

# Get the absolute path to the templates directory
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

# Only configure settings if they haven't been configured yet
if not settings.configured:
    settings.configure(TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
    }], INSTALLED_APPS=['django.contrib.humanize'])
    django.setup() 