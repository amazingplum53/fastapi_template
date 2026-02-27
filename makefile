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
	source .config/secret/secrets.source && \
	pulumi config set --cwd ./.pulumi/ --stack $(STACK) --secret db:password "$$DB_PASSWORD"; \
	pulumi up --cwd ./.pulumi/ --stack $(STACK) --yes

destroy:
	pulumi destroy --cwd ./.pulumi/ --stack $(STACK) --yes

