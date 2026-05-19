SHELL := /bin/bash
PROJECT_NAME = fastapi_template


CONTAINER ?= server
ssh:
	docker exec -it $(CONTAINER) bash

shell:
	docker exec -it $(CONTAINER) python3 manage.py shell

logs:
	docker logs --follow $(CONTAINER)

restart:
	source .config/secret/secrets.source && \
	docker restart $(CONTAINER)

up:
	docker rm -f django-server database || true
	source .config/secret/secrets.source && \
	docker compose -f .devcontainer/compose.yml up django-server database


STACK ?= prod
deploy:
	source .config/secret/secrets.source && \
	pulumi config set --cwd ./.pulumi/ --stack $(STACK) --secret db:password "$$DB_PASSWORD"; \
	pulumi up --cwd ./.pulumi/ --stack $(STACK) --yes

destroy:
	pulumi destroy --cwd ./.pulumi/ --stack $(STACK) --yes

