# Rate My Legislator - Backend

This directory contains the backend scraping and data management functionality for the Hawaii Legislature rating platform.

## Structure

```
backend/
├── src/                    # Python source code
│   ├── models.py          # Database models
│   ├── database.py        # Database management
│   ├── scraper_utils.py   # Utility functions
│   ├── bill_scraper.py    # Bill scraping functionality
│   ├── member_scraper.py  # Member scraping functionality
│   ├── batch_scraper.py   # Batch scraping orchestration
│   └── main.py           # Main application entry point
├── data/                  # Database and data files
├── logs/                  # Application logs
├── tests/                 # Test files
└── requirements.txt       # Python dependencies
```

## Setup

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Run a test scrape:
   ```bash
   cd src
   python limited_scrape_2025.py
   ```

3. Run batch scraping:
   ```bash
   cd src
   python batch_scraper.py --mode test
   ```

## Features

- **Bill Scraping**: Comprehensive scraping of Hawaii Legislature bills
- **Member Scraping**: Legislator information and committee assignments
- **Batch Processing**: Efficient bulk scraping with rate limiting
- **Database Management**: SQLite database with proper schema
- **Cloudflare Bypass**: Uses cloudscraper to handle protected sites
- **Error Handling**: Robust retry logic and error recovery