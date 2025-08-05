# Makefile for InkWell project

.PHONY: help build up down logs shell migrate collectstatic createsuperuser test clean dev prod

# Default target
help:
	@echo "InkWell Docker Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev        - Start development environment"
	@echo "  make dev-down   - Stop development environment"
	@echo "  make dev-logs   - View development logs"
	@echo ""
	@echo "Production:"
	@echo "  make prod       - Start production environment"
	@echo "  make prod-down  - Stop production environment"
	@echo "  make prod-logs  - View production logs"
	@echo ""
	@echo "Database:"
	@echo "  make migrate    - Run database migrations"
	@echo "  make superuser  - Create superuser"
	@echo "  make shell      - Open Django shell"
	@echo ""
	@echo "Utilities:"
	@echo "  make static     - Collect static files"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean up containers and volumes"
	@echo "  make build      - Build Docker images"

# Development environment
dev:
	docker-compose -f docker-compose.dev.yml up -d
	@echo "🚀 Development server running at http://localhost:8000"

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

# Production environment
prod:
	docker-compose up -d
	@echo "🚀 Production server running at http://localhost"

prod-down:
	docker-compose down

prod-logs:
	docker-compose logs -f

# Database operations
migrate:
	docker-compose run --rm web python manage.py migrate

superuser:
	docker-compose run --rm web python manage.py createsuperuser

shell:
	docker-compose run --rm web python manage.py shell

# Utilities
static:
	docker-compose run --rm web python manage.py collectstatic --noinput

test:
	docker-compose run --rm web python manage.py test

build:
	docker-compose build

clean:
	docker-compose down -v
	docker system prune -f
	docker volume prune -f

# Install dependencies
install:
	pip install -r requirements.txt

# Local development (without Docker)
local:
	python manage.py runserver

local-migrate:
	python manage.py migrate

local-static:
	python manage.py collectstatic

local-superuser:
	python manage.py createsuperuser
