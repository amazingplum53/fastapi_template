
SERVICE ?= server

shell:
	$(COMPOSE) exec $(SERVICE) bash

logs:
	$(COMPOSE) logs --follow $(SERVICE)

test:
	$(COMPOSE) exec $(SERVICE) pytest 

restart:
	$(COMPOSE) restart $(SERVICE)

up:
	. .config/secret/secrets.source && \
	$(COMPOSE) up server database

npm_build:
	npx vite build --config frontend/vite.config.js


