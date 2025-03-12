SHELL := /bin/bash

PROJECT := PyProject

.PHONY: lint lint-ruff test run start-containers stop-containers

lint:
	@pre-commit run --all-files

lint-ruff:
	@pre-commit run ruff --all-files

migrations:
	@alembic upgrade head
run:
	@poetry run uvicorn src.main:app --host 0.0.0.0 --reload

start-containers:
	@docker-compose up --detach --build db
	@docker-compose up --detach --build backend

stop-containers:
	@docker-compose down

test:
	@poetry run pytest
