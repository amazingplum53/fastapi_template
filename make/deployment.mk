STACK ?= prod


deploy:
	. .config/secret/secrets.source && \
	pulumi config set --cwd ./.pulumi/ --stack $(STACK) --secret db:password "$$DB_PASSWORD"; \
	pulumi up --cwd ./.pulumi/ --stack $(STACK) --yes
	

destroy:
	pulumi destroy --cwd ./.pulumi/ --stack $(STACK) --yes

