"""
WSGI config for cdsse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings 


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cdsse.settings')

if not settings.DEBUG:
	os.system('python manage.py makemigrations --noinput')
	os.system('python manage.py migrate --noinput')
	os.system('python manage.py collectstatic --noinput')

application = get_wsgi_application()
