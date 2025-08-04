# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a **containerized data-scraper + static site** architecture for tracking Hawaii State Legislature performance:

- **Data Scraper** (`data-scraper/`): Python application that scrapes legislature data from the Hawaii State Legislature website and exports JSON files
- **Static Frontend** (`frontend/`): Gatsby.js React application that consumes JSON data and builds a static site for GitHub Pages deployment

The data flow is: Hawaii Legislature Website → Python Scraper → SQLite Database → JSON Export → Gatsby Static Site → GitHub Pages

## Essential Commands

### Docker-based Development (Primary Workflow)

```bash
# Build all containers
make build

# Start frontend development server (http://localhost:3000)
make up

# Run data scraping (automatically exports to frontend)
make scrape                                    # Limited test scrape
make scrape-full                              # Full year scraping  
IDS='1-250' YEAR='2025' make scrape-members   # Range scrape members
NUMBERS='1-100' TYPES='SB HB' YEAR='2025' make scrape-bills  # Range scrape bills
make export-data                              # Export database to JSON files for frontend

# Build and deploy to GitHub Pages
make deploy

# Access container shells for debugging
make scraper-shell        # Data scraper container
make frontend-shell       # Frontend container
```

### Frontend Development Commands

**IMPORTANT: Always use Docker/Make commands for frontend development to avoid permission issues with npm creating root-owned files in .cache and node_modules directories.**

Use Docker commands (preferred):
```bash
make up                  # Start frontend dev server (http://localhost:3000)
make frontend-shell      # Access frontend container shell for debugging
make build-static        # Build static site for GitHub Pages
make deploy              # Deploy to GitHub Pages
```

Direct npm commands (avoid - use only in container):
```bash
cd frontend

# Development (use make up instead)
npm run develop           # Start Gatsby dev server
npm run typecheck        # TypeScript checking
npm run lint             # ESLint checking
npm run format           # Prettier formatting

# Production builds (use make build-static instead)
npm run build:github     # Build for GitHub Pages deployment
npm run deploy           # Deploy to GitHub Pages
```

### Data Scraper Commands

```bash
# Run tests
make test                # Runs data-scraper/src/test_schema.py

# Python scripts (run in container via make commands above)
python src/limited_scrape_2025.py    # Quick test scrape
python src/batch_scraper.py --mode both --year 2025  # Full scrape
python src/data_exporter.py          # Export to JSON
```

## Database Schema

SQLite database with SQLAlchemy ORM in `data-scraper/src/models.py`:

- **Member**: Persistent member information across years
- **MemberTerm**: Year-specific member data (party, district, contact)
- **MemberCommittee**: Committee assignments
- **Bill**: Main bill information with metadata
- **BillStatusUpdate**: Chronological status history
- **BillVersion**: Different bill versions (SD1, HD1, CD1, etc.)
- **BillCommitteeReport**: Committee reports with document links

## Data Export System

The scraper exports data to `frontend/src/data/` as JSON files via `data_exporter.py`:

- `summary.json` - Overall statistics and metadata
- `bills_YYYY.json` - Bills data organized by year
- `bills_all.json` - All bills summary (lighter version)
- `members.json` - Member information with latest terms
- `recent_activity.json` - Recent legislative activity
- `analytics.json` - Data for charts and visualizations

## Key Technical Details

### Data Scraping
- Uses `cloudscraper` to bypass Cloudflare protection
- Handles all bill types: SB, HB, SR, HR, SCR, HCR, GM
- Supports historical data from 2008 to present
- Containerized to avoid dependency conflicts

### Frontend Technology
- Gatsby.js for static site generation
- TypeScript for type safety
- Configured for GitHub Pages deployment with `--prefix-paths`
- React components for data visualization
- Responsive design for mobile compatibility

### Container Configuration
- `docker-compose.yml` defines three services:
  - `data-scraper`: Python scraping container
  - `frontend-dev`: Gatsby development server
  - `frontend-build`: Production build container
- Volume mounts enable live development and data sharing
- Health checks ensure scraper container is functional

## Testing and Code Quality

- **Frontend**: ESLint, TypeScript checking, Prettier formatting
- **Data Scraper**: Python schema validation tests
- **Integration**: Health checks verify database connectivity

Always run `make test` and frontend linting commands before committing changes.

## Deployment

GitHub Pages deployment requires updating `frontend/gatsby-config.ts` with correct repository information. The static site is built with `--prefix-paths` for proper GitHub Pages routing.

Important! Don't run sudo commands directly, as me to run them for you because you won't be able to run them directly.

If you think of tooling you think I should use to improve my process, please suggest it to me.

For git commits messages, don't include anything about claude
