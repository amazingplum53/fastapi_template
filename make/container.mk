
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


