# Makefile for Wagtail Starter Kit

-include .env
export  # Export all .env vars to sub-processes (uv run, etc.)

# Database selection: sqlite (default), postgres, mysql
DATABASE ?= sqlite
ifeq ($(DATABASE),postgres)
    COMPOSE_DB_FILE := docker/compose.postgresql.override.yaml
else ifeq ($(DATABASE),mysql)
    COMPOSE_DB_FILE := docker/compose.mysql.override.yaml
else
    COMPOSE_DB_FILE := docker/compose.sqlite3.override.yaml
endif

# --env-file ensures .env is used for variable substitution in compose files
DC := docker compose --env-file .env -f docker/compose.yaml -f $(COMPOSE_DB_FILE)

.PHONY: help
help:
	@echo "Usage: make [target] [DATABASE=sqlite|postgres|mysql]"
	@echo ""
	@echo "Development"
	@echo "  dev          Run locally (SQLite, uv, npm HMR + Django)"
	@echo "  up           Run in Docker (build image, migrate, start)"
	@echo "  down         Stop Docker services"
	@echo "  sh           Shell into the app container"
	@echo "  logs         Tail app container logs"
	@echo ""
	@echo "Maintenance"
	@echo "  reset        Reset local database and migrations"
	@echo "  clean        Remove all generated files"
	@echo "  test         Run Django tests inside Docker"
	@echo ""

.PHONY: check-env
check-env:
	@if [ ! -f .env ]; then \
		echo "Error: .env not found. Copy .env.example → .env and fill in values."; \
		exit 1; \
	fi

# ── Local development ─────────────────────────────────────────────────────────

.PHONY: dev
dev: check-env
	npm install && npm run build
	uv sync
	uv run python manage.py migrate --settings=app.settings.dev
	uv run python manage.py runserver --settings=app.settings.dev

# ── Docker ────────────────────────────────────────────────────────────────────

.PHONY: up
up: check-env
	$(DC) up -d --build
	$(DC) exec app python manage.py migrate

.PHONY: down
down:
	$(DC) down

.PHONY: sh
sh:
	$(DC) exec app bash

.PHONY: logs
logs:
	$(DC) logs -f app

# ── Maintenance ───────────────────────────────────────────────────────────────

.PHONY: reset
reset:
	@echo "Resetting local database and migrations..."
	@rm -f db.sqlite3
	@find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@find . -path "*/migrations/*.pyc" -delete
	@uv run python manage.py makemigrations --settings=app.settings.dev
	@uv run python manage.py migrate --settings=app.settings.dev
	@echo "Done."

.PHONY: clean
clean:
	@echo "Cleaning generated files..."
	@rm -rf ./node_modules ./static ./static_compiled ./media db.sqlite3 .venv
	@echo "Done."

.PHONY: test
test:
	$(DC) exec app python manage.py test
