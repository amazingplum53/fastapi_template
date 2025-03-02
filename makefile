
ssh:
	docker exec -it server bash

django-shell:
	docker exec -it server python3 manage.py shell

server-logs:
	docker logs --follow server