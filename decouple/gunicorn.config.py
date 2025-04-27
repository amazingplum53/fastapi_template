
"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ, path
from sys import path
from secret_keys import get_secret, create_secret_file, load_secrets_file, SECRETS_FILE_NAME, FILE_PATH

max_workers = cpu_count

bind = '0.0.0.0:' + environ.get('PORT', '8000')

max_requests = 1000

workers = max_workers()

path.append("/server/decouple/")

environ.setdefault('DJANGO_SETTINGS_MODULE', 'decouple.settings')

preload_app = True


def on_starting(server):
    
    if not path.exists(f"{FILE_PATH}/{SECRETS_FILE_NAME}"):

        secrets = get_secret()

        create_secret_file(secrets)

        load_secrets_file()

    else:
        load_secrets_file()
