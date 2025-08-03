# Rate My Legislator - Data Scraper

This directory contains the data scraping and export functionality for the Hawaii Legislature platform. The data scraper runs in a Docker container and exports JSON files for the static frontend.

## Structure

```
data-scraper/
├── src/                    # Python source code
│   ├── models.py          # Database models
│   ├── database.py        # Database management
│   ├── scraper_utils.py   # Utility functions
│   ├── bill_scraper.py    # Bill scraping functionality
│   ├── member_scraper.py  # Member scraping functionality
│   ├── batch_scraper.py   # Batch scraping orchestration
│   ├── data_exporter.py   # Data export to JSON for frontend
│   └── main.py           # Main application entry point
├── data/                  # Database and data files
├── logs/                  # Application logs
├── tests/                 # Test files
├── Dockerfile            # Container configuration
└── requirements.txt       # Python dependencies
```

## Usage with Docker (Recommended)

The data scraper is designed to run in a Docker container to avoid dependency conflicts.

### Quick Start

```bash
# From project root
make build          # Build Docker images
make scrape         # Run limited scrape
make export-data    # Export data to JSON files
```

### Available Commands

```bash
make scrape          # Run limited test scrape
make scrape-full     # Run comprehensive scraping for current year
make export-data     # Export database to JSON files
make scrape-and-export  # Combined scrape + export workflow
make test            # Run data scraper tests
make scraper-shell   # Access scraper container shell
```

## Manual Setup (Alternative)

If you prefer to run without Docker:

1. Install dependencies:
   ```bash
   cd data-scraper
   pip install -r requirements.txt
   ```

2. Run a test scrape:
   ```bash
   cd src
   python limited_scrape_2025.py
   ```

3. Export data for frontend:
   ```bash
   cd src
   python data_exporter.py
   ```

## Features

- **Comprehensive Scraping**: All bill types (SB, HB, SR, HR, SCR, HCR, GM) with full status history
- **Member Information**: Complete member profiles with district info and committee assignments
- **Historical Data**: Supports scraping from 2008 to present
- **Cloudflare Bypass**: Uses cloudscraper to handle 403 errors
- **Data Export**: Generates optimized JSON files for static site consumption
- **Docker Isolation**: Runs in container to avoid dependency conflicts
- **Batch Processing**: Efficient bulk scraping with rate limiting
- **Database Management**: SQLite database with proper schema
- **Error Handling**: Robust retry logic and error recovery

## Data Export

The data exporter (`data_exporter.py`) generates JSON files optimized for the static frontend:

### Export Files

- `summary.json` - Overall statistics and metadata
- `bills_YYYY.json` - Bills data organized by year
- `bills_all.json` - All bills summary (lighter version)
- `members.json` - Member information with latest terms
- `recent_activity.json` - Recent legislative activity
- `analytics.json` - Data for charts and visualizations

### Export Location

By default, data is exported to `../frontend/src/data/`. This can be configured with the `EXPORT_DIR` environment variable.

## Development

### Running Individual Components

```bash
# Access container shell
make scraper-shell

# Inside container:
python src/bill_scraper.py      # Test bill scraping
python src/member_scraper.py    # Test member scraping
python src/batch_scraper.py --mode test  # Run batch test
python src/data_exporter.py     # Export all data
```

### Database Management

The scraper uses SQLite by default, stored in the `data/` directory. The database is automatically created on first run.

### Logging

Logs are stored in the `logs/` directory and also displayed in the container output.

## Deployment Workflow

For production data updates:

1. **Scrape Data**: `make scrape-full` (comprehensive scraping)
2. **Export Data**: `make export-data` (generate JSON files)
3. **Commit Data**: Commit the generated JSON files to git
4. **Deploy**: The frontend will automatically rebuild with new data

## Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string (default: SQLite)
- `EXPORT_DIR`: Directory for exported JSON files
- `PYTHONPATH`: Python path configuration
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING)

### Rate Limiting

The scraper includes built-in rate limiting to be respectful to the Hawaii Legislature website. Default delay is 1 second between requests.