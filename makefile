SHELL := /bin/bash

ssh:
	docker exec -it server bash

shell:
	docker exec -it server python3 manage.py shell

logs:
	docker logs --follow server

restart:
	docker restart server

deploy:
	source decouple/secret/secrets.source && \
	pulumi up --cwd ./.pulumi/

destroy:
	source decouple/secret/secrets.source && \
	pulumi destroy --cwd ./.pulumi/

