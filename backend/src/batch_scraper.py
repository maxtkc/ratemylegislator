#!/usr/bin/env python3
"""
Batch scraping scripts for Hawaii Legislature data
"""

import argparse
import time
from datetime import datetime
from bill_scraper import BillScraper
from member_scraper import MemberScraper
from scraper_utils import ScrapingStats, setup_logging, validate_year
from database import DatabaseManager

class BatchScraper:
    def __init__(self, delay=0.5):
        self.bill_scraper = BillScraper()
        self.member_scraper = MemberScraper()
        self.db_manager = DatabaseManager()
        self.delay = delay
        self.logger = setup_logging()
        self.stats = ScrapingStats()
        
        # Bill types to scrape
        self.bill_types = ['SB', 'HB', 'SR', 'HR', 'SCR', 'HCR', 'GM']
    
    def scrape_bills_for_year(self, year, bill_types=None, start_number=1, max_number=10000):
        """Scrape all bills for a given year"""
        if bill_types is None:
            bill_types = self.bill_types
        
        self.logger.info(f"Starting bill scraping for year {year}")
        self.stats.reset()
        
        for bill_type in bill_types:
            self.logger.info(f"Scraping {bill_type} bills for {year}")
            consecutive_404s = 0
            bill_number = start_number
            
            while consecutive_404s < 2 and bill_number <= max_number:
                self.stats.record_attempt()
                
                try:
                    success = self.bill_scraper.scrape_bill(bill_type, bill_number, year)
                    
                    if success:
                        consecutive_404s = 0
                        self.stats.record_success()
                    else:
                        consecutive_404s += 1
                        self.stats.record_failure()
                        self.logger.debug(f"404 #{consecutive_404s} for {bill_type}{bill_number}-{year}")
                
                except Exception as e:
                    self.logger.error(f"Error scraping {bill_type}{bill_number}-{year}: {e}")
                    consecutive_404s += 1
                    self.stats.record_failure()
                
                bill_number += 1
                time.sleep(self.delay)
                
                # Progress reporting
                if bill_number % 100 == 0:
                    self.logger.info(f"Progress: {bill_type} {bill_number} ({self.stats.total_successful} successful)")
            
            self.logger.info(f"Completed {bill_type} for {year} (stopped at {bill_number})")
        
        self.stats.print_summary()
        self.logger.info(f"Completed bill scraping for year {year}")
    
    def scrape_members_for_year(self, year, start_id=1, end_id=1500, batch_size=50):
        """Scrape all members for a given year"""
        self.logger.info(f"Starting member scraping for year {year} (IDs {start_id}-{end_id})")
        self.stats.reset()
        
        for member_id in range(start_id, end_id + 1):
            self.stats.record_attempt()
            
            try:
                success = self.member_scraper.scrape_member(member_id, year)
                
                if success:
                    self.stats.record_success()
                else:
                    self.stats.record_failure()
            
            except Exception as e:
                self.logger.error(f"Error scraping member {member_id}-{year}: {e}")
                self.stats.record_failure()
            
            time.sleep(self.delay)
            
            # Progress reporting
            if member_id % batch_size == 0:
                self.logger.info(f"Progress: Member {member_id}/{end_id} ({self.stats.total_successful} successful)")
        
        self.stats.print_summary()
        self.logger.info(f"Completed member scraping for year {year}")
    
    def scrape_recent_bills(self, years=None, bill_types=None):
        """Scrape bills for recent years"""
        if years is None:
            current_year = datetime.now().year
            years = [current_year, current_year - 1]
        
        for year in years:
            self.scrape_bills_for_year(year, bill_types)
    
    def scrape_recent_members(self, years=None):
        """Scrape members for recent years"""
        if years is None:
            current_year = datetime.now().year
            years = [current_year, current_year - 1]
        
        for year in years:
            self.scrape_members_for_year(year)
    
    def scrape_specific_bills(self, bill_list):
        """Scrape specific bills from a list of (bill_type, bill_number, year) tuples"""
        self.logger.info(f"Scraping {len(bill_list)} specific bills")
        self.stats.reset()
        
        for bill_type, bill_number, year in bill_list:
            self.stats.record_attempt()
            
            try:
                success = self.bill_scraper.scrape_bill(bill_type, bill_number, year)
                
                if success:
                    self.stats.record_success()
                else:
                    self.stats.record_failure()
            
            except Exception as e:
                self.logger.error(f"Error scraping {bill_type}{bill_number}-{year}: {e}")
                self.stats.record_failure()
            
            time.sleep(self.delay)
        
        self.stats.print_summary()
    
    def scrape_specific_members(self, member_list):
        """Scrape specific members from a list of (member_id, year) tuples"""
        self.logger.info(f"Scraping {len(member_list)} specific members")
        self.stats.reset()
        
        for member_id, year in member_list:
            self.stats.record_attempt()
            
            try:
                success = self.member_scraper.scrape_member(member_id, year)
                
                if success:
                    self.stats.record_success()
                else:
                    self.stats.record_failure()
            
            except Exception as e:
                self.logger.error(f"Error scraping member {member_id}-{year}: {e}")
                self.stats.record_failure()
            
            time.sleep(self.delay)
        
        self.stats.print_summary()
    
    def full_historical_scrape(self, start_year=2008, end_year=None):
        """Perform a complete historical scrape of all data"""
        if end_year is None:
            end_year = datetime.now().year
        
        self.logger.info(f"Starting full historical scrape from {start_year} to {end_year}")
        
        # First scrape all bills
        for year in range(start_year, end_year + 1):
            self.logger.info(f"=== SCRAPING BILLS FOR YEAR {year} ===")
            self.scrape_bills_for_year(year)
        
        # Then scrape all members
        for year in range(start_year, end_year + 1):
            self.logger.info(f"=== SCRAPING MEMBERS FOR YEAR {year} ===")
            self.scrape_members_for_year(year)
        
        self.logger.info("Full historical scrape completed!")
    
    def update_recent_data(self):
        """Update with recent data (current and previous year)"""
        current_year = datetime.now().year
        years = [current_year, current_year - 1]
        
        self.logger.info("Updating recent data...")
        
        # Update bills
        for year in years:
            self.scrape_bills_for_year(year)
        
        # Update members
        for year in years:
            self.scrape_members_for_year(year)
    
    def test_scraping(self):
        """Test scraping with a small sample"""
        self.logger.info("Testing scraping with sample data...")
        
        # Test a few bills
        test_bills = [
            ("SB", 1, 2025),
            ("HB", 1, 2025),
            ("SB", 1300, 2025)
        ]
        self.scrape_specific_bills(test_bills)
        
        # Test a few members
        test_members = [
            (1, 2025),
            (7, 2025),
            (253, 2025)
        ]
        self.scrape_specific_members(test_members)

def main():
    parser = argparse.ArgumentParser(description='Hawaii Legislature Batch Scraper')
    parser.add_argument('--mode', choices=['bills', 'members', 'both', 'test', 'full', 'update'], 
                        default='test', help='Scraping mode')
    parser.add_argument('--year', type=int, help='Specific year to scrape')
    parser.add_argument('--start-year', type=int, default=2008, help='Start year for historical scrape')
    parser.add_argument('--end-year', type=int, help='End year for scraping')
    parser.add_argument('--bill-types', nargs='+', help='Bill types to scrape', 
                        choices=['SB', 'HB', 'SR', 'HR', 'SCR', 'HCR', 'GM'])
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between requests (seconds)')
    parser.add_argument('--start-id', type=int, default=1, help='Start member ID')
    parser.add_argument('--end-id', type=int, default=1500, help='End member ID')
    parser.add_argument('--max-bills', type=int, default=10000, help='Maximum bill number to try')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = BatchScraper(delay=args.delay)
    
    # Determine year range
    if args.end_year is None:
        args.end_year = datetime.now().year
    
    if args.year:
        years = [args.year]
    else:
        years = list(range(args.start_year, args.end_year + 1))
    
    # Execute based on mode
    if args.mode == 'test':
        scraper.test_scraping()
    
    elif args.mode == 'bills':
        for year in years:
            scraper.scrape_bills_for_year(year, args.bill_types, max_number=args.max_bills)
    
    elif args.mode == 'members':
        for year in years:
            scraper.scrape_members_for_year(year, args.start_id, args.end_id)
    
    elif args.mode == 'both':
        for year in years:
            scraper.scrape_bills_for_year(year, args.bill_types, max_number=args.max_bills)
            scraper.scrape_members_for_year(year, args.start_id, args.end_id)
    
    elif args.mode == 'full':
        scraper.full_historical_scrape(args.start_year, args.end_year)
    
    elif args.mode == 'update':
        scraper.update_recent_data()

if __name__ == "__main__":
    main()