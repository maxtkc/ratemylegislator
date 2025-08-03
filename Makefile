# Rate My Legislator - Docker Commands

.PHONY: help build up down logs clean test scraper frontend build-static deploy

# Default target
help:
	@echo "Available commands:"
	@echo "  build          - Build all Docker images"
	@echo "  up             - Start frontend development server"
	@echo "  down           - Stop all services"
	@echo "  logs           - View logs from all services"
	@echo "  clean          - Clean up Docker resources"
	@echo "  test           - Run data-scraper tests"
	@echo "  scraper        - Start data-scraper service"
	@echo "  frontend       - Start frontend development server"
	@echo "  build-static   - Build static site for GitHub Pages"
	@echo "  deploy         - Deploy to GitHub Pages"
	@echo "  scrape         - Run a limited scrape"
	@echo "  scrape-full    - Run full data scraping"
	@echo "  export-data    - Export scraped data to JSON for frontend"

# Build all images
build:
	docker-compose build

# Start development environment (frontend only)
up:
	docker-compose up -d frontend-dev

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
	docker-compose run --rm data-scraper python src/test_schema.py

# Data scraper service
scraper:
	docker-compose up -d data-scraper

# Frontend development only
frontend:
	docker-compose up -d frontend-dev

# Build static site for deployment
build-static:
	docker-compose --profile build run --rm frontend-build

# Deploy to GitHub Pages (run locally)
deploy:
	cd frontend && npm run deploy

# Run limited scrape
scrape:
	docker-compose run --rm data-scraper python src/limited_scrape_2025.py

# Run full scrape
scrape-full:
	docker-compose run --rm data-scraper python src/batch_scraper.py --mode both --year 2025

# Export data to frontend
export-data:
	docker-compose run --rm data-scraper python src/data_exporter.py

# Combined workflow: scrape and export
scrape-and-export:
	make scrape
	make export-data

# Install frontend dependencies
frontend-install:
	docker-compose run --rm frontend-dev npm install

# Data scraper shell
scraper-shell:
	docker-compose exec data-scraper /bin/bash

# Frontend shell
frontend-shell:
	docker-compose exec frontend-dev /bin/sh