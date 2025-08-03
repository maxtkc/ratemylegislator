# Rate My Legislator

A static website for tracking Hawaii State Legislature performance, built with containerized data scraping and static site generation for GitHub Pages deployment.

## Project Architecture

This project follows a **data-scraper + static site** architecture:

- **Data Scraper**: Containerized Python application that scrapes legislature data and exports JSON files
- **Static Frontend**: Gatsby.js application that consumes JSON data and builds a static site for GitHub Pages

```
ratemylegislator/
├── data-scraper/          # Python scraping and data management
│   ├── src/              # Source code including data export
│   ├── data/             # Database files
│   ├── logs/             # Application logs
│   └── Dockerfile        # Container configuration
├── frontend/              # Gatsby.js static site generator
│   ├── src/              # React components and pages
│   │   └── data/         # JSON files exported from data-scraper
│   ├── Dockerfile        # Container configuration
│   └── package.json      # Dependencies and build scripts
├── examples/              # Example HTML pages from legislature site
├── docker-compose.yml     # Container orchestration
├── Makefile              # Development commands
└── README.md             # This file
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Development Workflow

1. **Clone and Build**:
   ```bash
   git clone <repository-url>
   cd ratemylegislator
   make build
   ```

2. **Scrape Data**:
   ```bash
   make scrape          # Run limited scrape for testing
   make export-data     # Export data to JSON for frontend
   ```

3. **Start Development Server**:
   ```bash
   make up              # Start Gatsby development server on http://localhost:3000
   ```

4. **Build for Production**:
   ```bash
   make build-static    # Build static site for GitHub Pages
   ```

## Data Scraper

The data scraper is a containerized Python application that handles all data collection and processing.

### Features

- **Comprehensive Scraping**: All bill types (SB, HB, SR, HR, SCR, HCR, GM) with full status history
- **Member Information**: Complete member profiles with district info and committee assignments
- **Historical Data**: Supports scraping from 2008 to present
- **Cloudflare Bypass**: Uses cloudscraper to handle 403 errors
- **Data Export**: Generates optimized JSON files for static site consumption
- **Docker Isolation**: Runs in container to avoid dependency conflicts

### Available Commands

```bash
make scrape          # Run limited test scrape
make scrape-full     # Run comprehensive scraping for current year
make export-data     # Export database to JSON files
make scrape-and-export  # Combined scrape + export workflow
make test            # Run data scraper tests
make scraper-shell   # Access scraper container shell
```

### Data Export

The scraper exports data to `frontend/src/data/` as JSON files:

- `summary.json` - Overall statistics and metadata
- `bills_YYYY.json` - Bills data organized by year
- `bills_all.json` - All bills summary (lighter version)
- `members.json` - Member information with latest terms
- `recent_activity.json` - Recent legislative activity
- `analytics.json` - Data for charts and visualizations

## Static Frontend

The frontend is a Gatsby.js application optimized for GitHub Pages deployment.

### Features

- **Static Generation**: Pre-built pages for fast loading
- **GitHub Pages Ready**: Configured for seamless deployment
- **Responsive Design**: Mobile-friendly interface
- **Data Visualization**: Charts and graphs showing legislative trends
- **Search & Filter**: Browse bills and members efficiently
- **Performance Optimized**: Lazy loading and code splitting

### Development Commands

```bash
make frontend        # Start development server
make build-static    # Build for GitHub Pages
make frontend-shell  # Access frontend container shell
```

### Local Development

```bash
cd frontend
npm install
npm run develop      # Start local development
npm run build:github # Build for GitHub Pages
npm run deploy       # Deploy to GitHub Pages (requires setup)
```

## Deployment to GitHub Pages

### Setup

1. **Configure Repository**:
   - Update `frontend/gatsby-config.ts` with your GitHub username/repository
   - Ensure GitHub Pages is enabled in repository settings

2. **Deploy**:
   ```bash
   # Method 1: Using make command
   make deploy
   
   # Method 2: Manual build and deploy
   make build-static
   cd frontend
   npm run deploy
   ```

### GitHub Actions (Optional)

You can set up GitHub Actions to automatically build and deploy when you push to main:

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install and build
        run: |
          cd frontend
          npm ci
          npm run build:github
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/public
```

## Database Schema

- **Bills**: Main bill information with versions, titles, and metadata
- **Bill Status Updates**: Complete chronological status history
- **Bill Versions**: Different bill versions (SD1, HD1, CD1, etc.) with URLs
- **Bill Committee Reports**: Committee reports with document links
- **Members**: Persistent member information across years
- **Member Terms**: Year-specific information (party, district, contact info)
- **Member Committees**: Committee assignments and positions

## Examples

The `examples/` directory contains sample HTML pages from the Hawaii Legislature website:

- `SB1300-2025.html` - Example bill page
- `Member253-2025.html` - Example member page

These are useful for understanding the structure of the source data.

## Development Tips

### Adding New Features

1. **Data Changes**: Modify scrapers in `data-scraper/src/`
2. **Frontend Changes**: Add React components in `frontend/src/`
3. **Database Changes**: Update models in `data-scraper/src/models.py`

### Testing

```bash
make test            # Test data scraper
cd frontend && npm test  # Test frontend (when tests are added)
```

### Debugging

```bash
make scraper-shell   # Access data scraper container
make frontend-shell  # Access frontend container
make logs           # View all container logs
```

## Data Privacy

This project scrapes publicly available data from the Hawaii Legislature website. All data collected is from public records and official government sources.

## Legal Notice

This tool is for educational and research purposes. Please respect the Hawaii Legislature website's terms of service and scrape responsibly.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes and test with Docker
4. Update documentation if needed
5. Submit a pull request

## License

[Add your preferred license here]