

db_current:
	$(COMPOSE) exec server alembic current

db_upgrade:
	$(COMPOSE) exec server alembic upgrade head

MESSAGE := 
db_revision:
	$(COMPOSE) exec server alembic revision --autogenerate -m "$(MESSAGE)"
