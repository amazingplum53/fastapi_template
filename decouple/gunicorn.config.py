
"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ
from subprocess import run
from sys import path
from json import load

max_workers = cpu_count

bind = '0.0.0.0:' + environ.get('PORT', '8000')

max_requests = 1000

workers = max_workers()

path.append("/var/www/portfolio")

environ.setdefault('DJANGO_SETTINGS_MODULE', 'decouple.settings')

preload_app = True
