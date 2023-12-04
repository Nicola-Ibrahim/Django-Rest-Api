
lang:=en

.PHONY: superuser
superuser:
	poetry run python dj_rest_api/manage.py makesuperuser
users:
	poetry run python dj_rest_api/manage.py generate_users

.PHONY: lint
lint:
	poetry run pre-commit run --all-files


.PHONY: migrations
migrations:
	poetry run python dj_rest_api/manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python dj_rest_api/manage.py migrate

.PHONY: run-server
run-server:
	poetry run python dj_rest_api/manage.py runserver localhost:80


.PHONY: install
install:
	poetry install


.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall
	poetry run pre-commit install

.PHONY: update
update: migrations migrate	install-pre-commit


.PHONY: shell
shell:
	poetry run python dj_rest_api/manage.py shell_plus

.PHONY: flush-tokens
flush-tokens:
	poetry run python dj_rest_api/manage.py flushexpiredtokens.py

.PHONY: check-deploy
check-deploy:
	poetry run python dj_rest_api/manage.py check.py --deploy


.PHONY: db-graph
db-graph:
	poetry run python dj_rest_api/manage.py graph_models.py -a -g -o lineup_models_visualized.png


.PHONY: test
test:
	poetry run python -m pytest -v -rs -s -n auto --show-capture=no

.PHONY: test-cov
test-cov:
	poetry run python -m pytest --cov
	poetry run coverage html

.PHONY: dev-docker
dev-docker:
	docker-compose -f docker-compose.dev.yml up --build -d --force-recreate

.PHONY: prod-docker
prod-docker:
	docker-compose -f docker-compose.yml up --build -d --force-recreate

.PHONY: generate_key
generate_key:
	openssl rand -base64 32 > dj_rest_api/config/settings/.keys/jwtHS256.key


.PHONY: translate
translate:
	django-admin makemessages -l ${lang} --ignore .venv

.PHONY: compile-translate
compile-translate:
	django-admin compilemessages --ignore=.venv
