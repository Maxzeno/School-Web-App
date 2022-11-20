"""
WSGI config for cdsse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cdsse.settings')

os.system('python manage.py migrate')
os.system('python manage.py collectstatic')

application = get_wsgi_application()
