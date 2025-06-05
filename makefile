
ssh:
	docker exec -it server bash

django-shell:
	docker exec -it server python3 manage.py shell

logs:
	docker logs --follow server

restart:
	docker restart server

deploy:
	pulumi up --cwd ./.pulumi/

destroy:
	pulumi destroy --cwd ./.pulumi/

