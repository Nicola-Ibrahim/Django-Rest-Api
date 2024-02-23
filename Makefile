lang:=en

# Define the default value for the test file
test_file := None


.DEFAULT_GOAL := help
help: ## Show this help.
	fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

## superuser: Create a superuser for the Django application
.PHONY: superuser
superuser:
	poetry run python dj_rest_api/manage.py makesuperuser

## users: Generate dummy users for testing
.PHONY: users
users:
	poetry run python dj_rest_api/manage.py generate_users

## lint: Run pre-commit hooks for linting
.PHONY: lint
lint:
	poetry run pre-commit run --all-files


## migrations: Create database migrations
.PHONY: migrations
migrations:
	poetry run python dj_rest_api/manage.py makemigrations

## run-server: Run the Django development server
.PHONY: migrate
migrate:
	poetry run python dj_rest_api/manage.py migrate


## run-server: Run the Django development server
.PHONY: run-server
run-server:
	poetry run python dj_rest_api/manage.py runserver localhost:80


## install: Install project dependencies
.PHONY: install
install:
	poetry install

## install-pre-commit: Install pre-commit hooks
.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall
	poetry run pre-commit install

## update: Update project dependencies and apply migrations
.PHONY: update
update: migrations migrate	install-pre-commit

## shell: Open Django shell with additional models
.PHONY: shell
shell:
	poetry run python dj_rest_api/manage.py shell_plus

## check-deploy: Check deployment readiness
.PHONY: check-deploy
check-deploy:
	poetry run python dj_rest_api/manage.py check --deploy


.PHONY: db-graph
db-graph:
	poetry run python dj_rest_api/manage.py graph_models -a -g -o lineup_models_visualized.png

.PHONY: test
test:
ifeq ($(test_file),None)
	poetry run python -m pytest -v -rs -s -n auto --show-capture=no
else
	poetry run python -m pytest -v -rs -s -n auto --show-capture=no -k ${test_file}
endif

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


.PHONY: run-celery
run-celery:
	celery -A dj_rest_api worker --loglevel=info --pool=solo


.PHONY: show-urls
show-urls:
	poetry run python dj_rest_api\manage.py show_urls
