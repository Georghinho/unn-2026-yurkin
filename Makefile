.PHONY: install test check ruff-cs-check ruff-cs-fix ruff-linter-check ruff-linter-fix mypy-check build run

install:
	python -m pip install -r requirements-dev.txt

test:
	python -m unittest discover -s tests -v

ruff-cs-check:
	python -m ruff format --check .

ruff-cs-fix:
	python -m ruff format .

ruff-linter-check:
	python -m ruff check .

ruff-linter-fix:
	python -m ruff check --fix .

mypy-check:
	python -m mypy

check: ruff-cs-check ruff-linter-check mypy-check test

build:
	docker build -t telegram-echo-bot .

run:
	python -m bot
