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
	@echo "  deploy         - Build and deploy to GitHub Pages"
	@echo "  scrape         - Run limited scrape with data export"
	@echo "  scrape-full    - Run full data scraping with export"
	@echo "  scrape-members - Range scrape members: IDS='1-250' YEAR='2025' make scrape-members"
	@echo "  scrape-bills   - Range scrape bills: NUMBERS='1-100' TYPES='SB HB' YEAR='2025' make scrape-bills"
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

# Deploy to GitHub Pages
deploy:
	docker-compose --profile deploy run --rm frontend-deploy

# Run limited scrape
scrape:
	docker-compose run --rm --user root data-scraper bash -c "DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/limited_scrape_2025.py && DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/data_exporter.py"

# Run full scrape
scrape-full:
	docker-compose run --rm --user root data-scraper bash -c "DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/batch_scraper.py --mode both --year 2025 && DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/data_exporter.py"

# Run range-based member scraping
scrape-members:
	docker-compose run --rm --user root data-scraper bash -c "DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/batch_scraper.py --mode range-members --member-ids '$(IDS)' --years '$(YEAR)' --delay 0.8 && DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/data_exporter.py"

# Run range-based bill scraping  
scrape-bills:
	docker-compose run --rm --user root data-scraper bash -c "DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/batch_scraper.py --mode range-bills --bill-numbers '$(NUMBERS)' --bill-types $(TYPES) --years '$(YEAR)' --delay 0.8 && DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/data_exporter.py"

# Export data to frontend
export-data:
	docker-compose run --rm --user root data-scraper bash -c "DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/data_exporter.py"

# Combined workflow: scrape and export
scrape-and-export:
	docker-compose run --rm --user root data-scraper bash -c "DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/limited_scrape_2025.py && DATABASE_URL='sqlite:////tmp/hawaii_legislature.db' python src/data_exporter.py"

# Install frontend dependencies
frontend-install:
	docker-compose run --rm frontend-dev npm install

# Data scraper shell
scraper-shell:
	docker-compose exec data-scraper /bin/bash

# Frontend shell
frontend-shell:
	docker-compose exec frontend-dev /bin/sh