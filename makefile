PROJECT_NAME := fastapi_template
COMPOSE := docker compose -p $(PROJECT_NAME)_devcontainer -f .devcontainer/compose.yml
SERVICE ?= server

shell:
	$(COMPOSE) exec $(SERVICE) bash

logs:
	$(COMPOSE) logs --follow $(SERVICE)

restart:
	$(COMPOSE) restart $(SERVICE)

up:
	. .config/secret/secrets.source && \
	$(COMPOSE) up server database


STACK ?= prod
deploy:
	. .config/secret/secrets.source && \
	pulumi config set --cwd ./.pulumi/ --stack $(STACK) --secret db:password "$$DB_PASSWORD"; \
	pulumi up --cwd ./.pulumi/ --stack $(STACK) --yes

destroy:
	pulumi destroy --cwd ./.pulumi/ --stack $(STACK) --yes

