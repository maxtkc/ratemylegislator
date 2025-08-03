# Rate My Legislator - Docker Commands

.PHONY: help build up down logs clean test backend frontend frontend-prod

# Default target
help:
	@echo "Available commands:"
	@echo "  build         - Build all Docker images"
	@echo "  up            - Start development environment (backend + frontend-dev)"
	@echo "  down          - Stop all services"
	@echo "  logs          - View logs from all services"
	@echo "  clean         - Clean up Docker resources"
	@echo "  test          - Run tests"
	@echo "  backend       - Start only backend service"
	@echo "  frontend      - Start only frontend development"
	@echo "  frontend-prod - Start frontend in production mode"
	@echo "  scrape        - Run a limited scrape"

# Build all images
build:
	docker-compose build

# Start development environment
up:
	docker-compose up -d backend frontend-dev

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Clean up
clean:
	docker-compose down -v
	docker system prune -f

# Run tests
test:
	docker-compose run --rm backend python src/test_schema.py

# Backend only
backend:
	docker-compose up -d backend

# Frontend development only
frontend:
	docker-compose up -d frontend-dev

# Frontend production
frontend-prod:
	docker-compose --profile production up -d frontend-prod

# Run scraper
scrape:
	docker-compose run --rm backend python src/limited_scrape_2025.py

# Install frontend dependencies
frontend-install:
	docker-compose run --rm frontend-dev npm install

# Backend shell
backend-shell:
	docker-compose exec backend /bin/bash

# Frontend shell
frontend-shell:
	docker-compose exec frontend-dev /bin/sh