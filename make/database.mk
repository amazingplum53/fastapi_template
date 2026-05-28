config_path := app/database

db_current:
	$(COMPOSE) exec server python -m app.database.commands db_current

db_upgrade:
	$(COMPOSE) exec server python -m app.database.commands db_upgrade

MESSAGE :=
db_revision:
	$(COMPOSE) exec server python -m app.database.commands db_revision "$(MESSAGE)"

db_shell:
	$(COMPOSE) exec database psql -U local_db
