"""Gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
import os
import sys

sys.path.append("/server/decouple/")

from decouple.secret.keys import handle_secrets

max_workers = cpu_count()

bind = '0.0.0.0:' + os.environ.get('PORT', '8000')

max_requests = 1000

workers = max_workers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decouple.settings')

ALB_DNS_NAME = os.getenv("ALB_DNS_NAME", "")

STACK = os.getenv("STACK", "local")

print(f"Using {STACK} env file")

preload_app = True

handle_secrets(STACK)
