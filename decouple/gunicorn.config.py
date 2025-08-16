"""Gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
import os
import sys

sys.path.append("/server/decouple/")

from decouple.secret.keys import handle_secrets

bind = '0.0.0.0:' + os.environ.get('PORT', '8000')

# Concurrency
threads = 1
max_workers = cpu_count()
workers = max_workers

# Timeouts & keepalive
timeout = 60
graceful_timeout = 30
keepalive = 5

# Worker recycling
max_requests = 1000
max_requests_jitter = 100

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decouple.settings')

STACK = os.getenv("STACK", "local")

print(f"Using {STACK} env file")

preload_app = True

handle_secrets(STACK)
