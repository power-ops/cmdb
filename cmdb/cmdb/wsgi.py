"""
WSGI config for cmdb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import socketio
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb.settings')


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        settings.SOCKETIO.sleep(10)
        count += 1
        settings.SOCKETIO.emit('my_response', {'data': 'Server generated event'})


settings.SOCKETIO.start_background_task(background_thread)

django_app = get_wsgi_application()
application = socketio.WSGIApp(settings.SOCKETIO, django_app)
