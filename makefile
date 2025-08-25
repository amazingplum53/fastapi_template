SHELL := /bin/bash
PROJECT_NAME = fastapi_template
STACK ?= prod

ssh:
	docker exec -it server bash

shell:
	docker exec -it server python3 manage.py shell

logs:
	docker logs --follow server

restart:
	docker restart server

deploy:
	source $(PROJECT_NAME)/secret/secrets.source && \
	pulumi up --cwd ./.pulumi/ --stack $(STACK) --yes

destroy:
	source $(PROJECT_NAME)/secret/secrets.source && \
	pulumi destroy --cwd ./.pulumi/ --stack $(STACK) --yes

