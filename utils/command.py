
from app.asgi import bootstrap


def command():

    bootstrap()

    from app import settings

