config_path := app/database/alembic.ini

db_current:
	$(COMPOSE) exec server alembic -c config_path current

db_upgrade:
	$(COMPOSE) exec server alembic -c config_path upgrade head

MESSAGE := 
db_revision:
	$(COMPOSE) exec server alembic -c config_path revision --autogenerate -m "$(MESSAGE)"
