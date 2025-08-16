"""
WSGI config for decouple project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "decouple.settings")
_django_app = get_wsgi_application()

def application(environ, start_response):
    if environ.get("PATH_INFO") == "/health":
        start_response("204 No Content", [
            ("Content-Length", "0"),
            ("Content-Type", "text/plain; charset=utf-8"),
        ])
        return [b""]
    return _django_app(environ, start_response)
