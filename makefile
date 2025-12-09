.PHONY: install update build test lint format standards test coverage models

install:
	poetry install --with dev

update:
	poetry update

build:
	poetry build

lint:
	poetry run ruff check --fix . --config .ruff.toml

format:
	poetry run ruff format . --config .ruff.toml

standards:
	@make lint
	@echo "Code standards check complete."
	@make format
	@echo "Code formatting complete."

test:
	poetry run pytest

run:
	cd src/cezzis_com_bootstrapper && poetry run python -m cezzis_com_bootstrapper

coverage:
	poetry run pytest -v --cov=src/cezzis_com_bootstrapper --cov-report=xml:coverage.xml --cov-report=term --junitxml=pytest-results.xml

models:
	poetry run datamodel-codegen \
		--url "https://localhost:7176/scalar/v1/openapi.json" \
		--input-file-type openapi --output src/cezzis_com_bootstrapper/models/bootstrapper_models.py \
		--output-model-type pydantic_v2.BaseModel \
		--field-constraints --use-default \
		--use-schema-description \
		--target-python-version 3.12

all:
	@make install
	@make models
	@make standards
	@make coverage
	@make build