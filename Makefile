.PHONY: install test lint format build deploy-sam

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=backend --cov-report=term-missing

lint:
	ruff check backend/ tests/

format:
	ruff format backend/ tests/

build:
	cd infrastructure && sam build

deploy-sam:
	cd infrastructure && sam deploy --guided

local-api:
	cd infrastructure && sam local start-api

audit:
	pip-audit
