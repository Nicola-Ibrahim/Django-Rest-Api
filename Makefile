.PHONY: superuser
superuser:
	pipenv run python src\manage.py makesuperuser

.PHONY: lint
lint:
	pipenv run pre-commit run --all-files


.PHONY: migrations
migrations:
	poetry run python src\manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python src\manage.py migrate

.PHONY: run-server
run-server:
	poetry run python src\manage.py runserver 127.0.0.1:8000


.PHONY: install
install:
	poetry install


.PHONY: update-pre-commit
update-pre-commit:
	poetry run pre-commit uninstall
	poetry run pre-commit install

.PHONY: update
update: migrations migrate	update-pre-commit


.PHONY: shell
shell:
	pipenv run python manage shell_plus.py

.PHONY: flush-tokens
flush-tokens:
	pipenv run python manage flushexpiredtokens.py

.PHONY: check-deploy
check-deploy:
	pipenv run python manage check.py --deploy


.PHONY: db-graph
db-graph:
	pipenv run python manage graph_models.py -a -g -o lineup_models_visualized.png
