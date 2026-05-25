
from fastapi_template.asgi import bootstrap

bootstrap()

from fastapi_template import settings

print(settings.DATABASE)