.PHONY: superuser
superuser:
	poetry run python -m src.manage makesuperuser
users:
	poetry run python -m src.manage generate_users

.PHONY: lint
lint:
	poetry run pre-commit run --all-files


.PHONY: migrations
migrations:
	poetry run python -m src.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m src.manage migrate

.PHONY: run-server
run-server:
	poetry run python -m src.manage runserver 127.0.0.1:8000


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
	poetry run python -m src.manage shell_plus

.PHONY: flush-tokens
flush-tokens:
	poetry run python -m src.manage flushexpiredtokens.py

.PHONY: check-deploy
check-deploy:
	poetry run python -m src.manage check.py --deploy


.PHONY: db-graph
db-graph:
	poetry run python -m src.manage graph_models.py -a -g -o lineup_models_visualized.png


.PHONY: test
test:
	poetry run python -m pytest -v -rs -s -n auto --show-capture=no

.PHONY: test-cov
test-cov:
	poetry run python -m pytest --cov
	poetry run coverage html

