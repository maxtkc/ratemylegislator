# Rate My Legislator

A comprehensive platform for tracking and rating Hawaii State Legislature performance, combining data scraping with an interactive web interface.

## Project Structure

```
ratemylegislator/
├── backend/                # Python scraping and data management
│   ├── src/               # Source code
│   ├── data/             # Database files
│   ├── logs/             # Application logs
│   └── tests/            # Test files
├── frontend/              # Gatsby.js web application (coming soon)
├── examples/              # Example HTML pages from legislature site
├── docs/                  # Documentation
└── README.md             # This file
```

## Backend (Data Scraping)

The backend handles comprehensive scraping of the Hawaii State Legislature website.

### Features

- **Comprehensive Bill Scraping**: All bill types (SB, HB, SR, HR, SCR, HCR, GM) with full status history
- **Member Information**: Complete member profiles with district info, contact details, and committee assignments
- **Historical Data**: Supports scraping from 2008 to present
- **Robust Database**: SQLAlchemy models with proper relationships and foreign keys
- **Error Handling**: Retry logic, rate limiting, and comprehensive logging
- **Cloudflare Bypass**: Uses cloudscraper to handle protected sites

### Quick Start

1. **Setup Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run Test Scrape**:
   ```bash
   cd backend/src
   python limited_scrape_2025.py
   ```

3. **Run Batch Scraping**:
   ```bash
   cd backend/src
   python batch_scraper.py --mode test
   ```

### Database Schema

- **Bills**: Main bill information with versions, titles, and metadata
- **Bill Status Updates**: Complete chronological status history
- **Bill Versions**: Different bill versions (SD1, HD1, CD1, etc.) with URLs
- **Bill Committee Reports**: Committee reports with document links
- **Members**: Persistent member information across years
- **Member Terms**: Year-specific information (party, district, contact info)
- **Member Committees**: Committee assignments and positions

## Frontend (Web Interface)

The frontend will be built with Gatsby.js to provide an interactive web interface for exploring legislative data.

### Planned Features

- **Legislator Profiles**: Detailed pages for each member with voting history
- **Bill Tracking**: Search and filter bills by type, status, and topic
- **Performance Metrics**: Rating system for legislator effectiveness
- **Data Visualization**: Charts and graphs showing legislative trends
- **Responsive Design**: Mobile-friendly interface
- **Fast Performance**: Static site generation with Gatsby

### Setup (Coming Soon)

```bash
cd frontend
npm install
npm start
```

## Examples

The `examples/` directory contains sample HTML pages from the Hawaii Legislature website:

- `SB1300-2025.html` - Example bill page
- `Member253-2025.html` - Example member page

These are useful for understanding the structure of the source data.

## Development

### Adding New Features

1. **Backend Changes**: Modify Python scrapers in `backend/src/`
2. **Frontend Changes**: Add React components in `frontend/src/` (coming soon)
3. **Database Changes**: Update models in `backend/src/models.py`

### Testing

```bash
# Test backend
cd backend/src
python test_schema.py

# Test frontend (coming soon)
cd frontend
npm test
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Data Privacy

This project scrapes publicly available data from the Hawaii Legislature website. All data collected is from public records and official government sources.

## Legal Notice

This tool is for educational and research purposes. Please respect the Hawaii Legislature website's terms of service and scrape responsibly.

## License

[Add your preferred license here]