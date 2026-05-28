from functools import wraps

from utils.keys import handle_secrets
from utils.variables import load_variables

def bootstrap():

    import sys
    import os

    STACK = os.getenv("STACK", "local")
    print(f"Using {STACK} env file")



    load_variables(STACK)

    handle_secrets(STACK)


def command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        bootstrap()

        from app import settings

        return func(*args, **kwargs)

    return wrapper