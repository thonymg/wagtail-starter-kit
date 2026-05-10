# Makefile for Wagtail Starter Kit

-include .env

# Database selection: sqlite (default), postgres, mysql
DATABASE ?= sqlite
ifeq ($(DATABASE),postgres)
    COMPOSE_DB_FILE := compose.postgresql.override.yaml
else ifeq ($(DATABASE),mysql)
    COMPOSE_DB_FILE := compose.mysql.override.yaml
else
    COMPOSE_DB_FILE := compose.sqlite3.override.yaml
endif

DC := docker compose -f compose.yaml -f $(COMPOSE_DB_FILE)

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Development"
	@echo "  dev          Run locally (SQLite, uv, npm)"
	@echo "  up           Run in Docker (builds and migrates)"
	@echo "  down         Stop Docker"
	@echo "  sh           Shell into Docker container"
	@echo ""
	@echo "Maintenance"
	@echo "  reset        Reset local database and migrations"
	@echo "  clean        Remove all generated files (node_modules, static, etc.)"
	@echo "  test         Run Django tests"
	@echo ""

# Internal: check environment
.PHONY: check-env
check-env:
	@if [ ! -f .env ]; then echo "Missing .env. Copy .env.example to .env"; exit 1; fi

# --- Development ---

.PHONY: dev
dev: check-env
	npm install && npm run build
	uv run python manage.py migrate
	uv run python manage.py runserver

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

# --- Maintenance ---

.PHONY: reset
reset:
	@echo "Resetting local database and migrations..."
	@rm -f db.sqlite3
	@find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@find . -path "*/migrations/*.pyc" -delete
	@uv run python manage.py makemigrations
	@uv run python manage.py migrate
	@echo "Reset complete."

.PHONY: clean
clean:
	@echo "Cleaning generated files..."
	@rm -rf ./node_modules ./static ./static_compiled ./media db.sqlite3
	@echo "Clean complete."

.PHONY: test
test:
	$(DC) exec app python manage.py test
