"""Gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
import os
import sys

sys.path.append("/server/decouple/")

from decouple.secret.keys import get_secret, create_secret_file, load_secrets_file, SECRETS_FILE_NAME, FILE_PATH

max_workers = cpu_count()

bind = '0.0.0.0:' + os.environ.get('PORT', '8000')

max_requests = 1000

workers = max_workers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decouple.settings')

APP_ENV = os.getenv("APP_ENV", "dev")

preload_app = True

def on_starting(server):

    if not os.path.exists(f"{FILE_PATH}/{SECRETS_FILE_NAME}.env"): 
        try:
            print(f"Fetching {APP_ENV} secrets")
            secrets = get_secret(APP_ENV)
            create_secret_file(secrets)
            load_secrets_file()
        except Exception as e:
            print("secrets not loaded:" + str(e))
    else:
        load_secrets_file()
