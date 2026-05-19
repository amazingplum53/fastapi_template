COMPOSE = docker compose -p fastapi_template_devcontainer -f .devcontainer/compose.yml
SERVICE ?= server
DB_SERVICE ?= database


ssh:
	$(COMPOSE) exec $(SERVICE) bash

logs:
	$(COMPOSE) logs --follow $(SERVICE)

restart:
	$(COMPOSE) restart $(SERVICE)

up:
	docker rm -f server database || true
	source .config/secret/secrets.source && \
	docker compose -f .devcontainer/compose.yml up server database


STACK ?= prod
deploy:
	source .config/secret/secrets.source && \
	pulumi config set --cwd ./.pulumi/ --stack $(STACK) --secret db:password "$$DB_PASSWORD"; \
	pulumi up --cwd ./.pulumi/ --stack $(STACK) --yes

destroy:
	pulumi destroy --cwd ./.pulumi/ --stack $(STACK) --yes

