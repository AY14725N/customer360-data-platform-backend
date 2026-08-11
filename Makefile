.PHONY: install test lint format run-api up down

install:
	python -m pip install -r requirements.txt

test:
	python -m pytest -q

lint:
	python -m ruff check .

format:
	python -m ruff format .

run-api:
	python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

up:
	docker compose up --build -d

down:
	docker compose down
