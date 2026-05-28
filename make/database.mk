config_path := app/database

db_init:
	$(COMPOSE) exec server alembic init $(config_path)/migrations

db_current:
	$(COMPOSE) exec server alembic -c $(config_path)/alembic.ini current

db_upgrade:
	$(COMPOSE) exec server alembic -c $(config_path)/alembic.ini upgrade head

MESSAGE := 
db_revision:
	$(COMPOSE) exec server alembic -c $(config_path)/alembic.ini revision --autogenerate -m "$(MESSAGE)"
