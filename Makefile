.PHONY: dev dev-api dev-ui install test lint

install:
	cd backend && uv sync
	cd frontend && npm install

dev:
	@trap 'kill 0' SIGINT; \
	$(MAKE) dev-api & \
	$(MAKE) dev-ui & \
	wait

dev-api:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

dev-ui:
	cd frontend && npm run dev

test:
	cd backend && uv run pytest

lint:
	cd backend && uv run ruff check . && uv run mypy .
