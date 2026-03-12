.PHONY: install init-db test run run-cloud

install:
	python -m pip install -e .[dev]

init-db:
	python -m app.init_db

test:
	pytest -q

run:
	uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

run-cloud:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
