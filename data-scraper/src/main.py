#!/usr/bin/env python3
"""
Hawaii Legislature Scraper
Main entry point for scraping Hawaii Capitol website data
"""

import argparse
from scraper import HawaiiLegislatureScraper
from database import init_database

def main():
    parser = argparse.ArgumentParser(description='Scrape Hawaii Legislature data')
    parser.add_argument('--init-db', action='store_true', help='Initialize database tables')
    parser.add_argument('--test', action='store_true', help='Run test scraping on a few items')
    parser.add_argument('--full', action='store_true', help='Run full scraping process')
    parser.add_argument('--year', type=int, help='Scrape specific year only')
    parser.add_argument('--bills-only', action='store_true', help='Scrape bills only')
    parser.add_argument('--members-only', action='store_true', help='Scrape members only')
    
    args = parser.parse_args()
    
    if args.init_db:
        print("Initializing database...")
        init_database()
        return
    
    scraper = HawaiiLegislatureScraper()
    
    if args.test:
        print("Running test scraping...")
        # Test a few bills and members
        scraper.scrape_bill("SB", 1, 2015)
        scraper.scrape_bill("HB", 1, 2015)
        scraper.scrape_member(7, 2025)
        scraper.scrape_member(1, 2025)
        
    elif args.full:
        print("Running full scraping process...")
        scraper.run_full_scrape()
        
    elif args.year:
        if args.bills_only:
            scraper.scrape_bills_for_year(args.year)
        elif args.members_only:
            scraper.scrape_members_for_year(args.year)
        else:
            scraper.scrape_bills_for_year(args.year)
            scraper.scrape_members_for_year(args.year)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()