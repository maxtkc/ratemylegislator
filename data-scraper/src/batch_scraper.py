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

def parse_range(range_str):
    """Parse range strings like '1-250', '1,5,10-20', or single numbers"""
    if not range_str:
        return []
    
    numbers = []
    parts = range_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-', 1))
            numbers.extend(range(start, end + 1))
        else:
            numbers.append(int(part))
    
    return sorted(set(numbers))

def parse_year_range(year_str):
    """Parse year range strings like '2024-2025' or '2025'"""
    if not year_str:
        return []
    
    if '-' in year_str:
        start, end = map(int, year_str.split('-', 1))
        return list(range(start, end + 1))
    else:
        return [int(year_str)]

class BatchScraper:
    def __init__(self, delay=0.5, max_workers=4):
        self.db_manager = DatabaseManager()
        self.db_manager.create_tables()  # Ensure tables exist
        self.bill_scraper = BillScraper(db_manager=self.db_manager)
        self.member_scraper = MemberScraper(db_manager=self.db_manager)
        self.delay = delay
        self.max_workers = max_workers
        self.logger = setup_logging()
        self.stats = ScrapingStats()
        
        # Bill types to scrape
        self.bill_types = ['SB', 'HB', 'SR', 'HR', 'SCR', 'HCR', 'GM']
    
    def scrape_bills_for_year(self, year, bill_types=None, start_number=1, max_number=10000):
        """Scrape all bills for a given year using multithreading"""
        if bill_types is None:
            bill_types = self.bill_types
        
        self.logger.info(f"Starting multithreaded bill scraping for year {year} (using {self.max_workers} threads)")
        self.stats.reset()
        
        for bill_type in bill_types:
            self.logger.info(f"Scraping {bill_type} bills for {year}")
            success_count = self.bill_scraper.scrape_bill_range(
                bill_type, year, start_number, max_number, self.max_workers
            )
            self.stats.total_successful += success_count
        
        self.stats.print_summary()
        self.logger.info(f"Completed bill scraping for year {year}")
    
    def scrape_members_for_year(self, year, start_id=1, end_id=1500, batch_size=50):
        """Scrape all members for a given year using multithreading"""
        self.logger.info(f"Starting multithreaded member scraping for year {year} (IDs {start_id}-{end_id}) (using {self.max_workers} threads)")
        self.stats.reset()
        
        success_count = self.member_scraper.scrape_member_range(
            year, start_id, end_id, self.max_workers
        )
        self.stats.total_successful = success_count
        
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
    
    def scrape_members_by_range(self, member_ids, years, batch_size=50):
        """Scrape members using lists of member IDs and years"""
        self.logger.info(f"Starting range-based member scraping: {len(member_ids)} IDs x {len(years)} years")
        self.stats.reset()
        
        total_combinations = len(member_ids) * len(years)
        processed = 0
        
        for year in years:
            for member_id in member_ids:
                self.stats.record_attempt()
                processed += 1
                
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
                if processed % batch_size == 0:
                    self.logger.info(f"Progress: {processed}/{total_combinations} ({self.stats.total_successful} successful)")
        
        self.stats.print_summary()
        self.logger.info(f"Completed range-based member scraping")
    
    def scrape_bills_by_range(self, bill_numbers, bill_types, years):
        """Scrape bills using lists of bill numbers, types, and years"""
        if not bill_types:
            bill_types = self.bill_types
        
        self.logger.info(f"Starting range-based bill scraping: {len(bill_numbers)} numbers x {len(bill_types)} types x {len(years)} years")
        self.stats.reset()
        
        total_combinations = len(bill_numbers) * len(bill_types) * len(years)
        processed = 0
        
        for year in years:
            for bill_type in bill_types:
                for bill_number in bill_numbers:
                    self.stats.record_attempt()
                    processed += 1
                    
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
                    
                    # Progress reporting
                    if processed % 100 == 0:
                        self.logger.info(f"Progress: {processed}/{total_combinations} ({self.stats.total_successful} successful)")
        
        self.stats.print_summary()
        self.logger.info(f"Completed range-based bill scraping")
    
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
    parser.add_argument('--mode', choices=['bills', 'members', 'both', 'test', 'full', 'update', 'range-members', 'range-bills'], 
                        default='test', help='Scraping mode')
    parser.add_argument('--year', type=int, help='Specific year to scrape')
    parser.add_argument('--start-year', type=int, default=2008, help='Start year for historical scrape')
    parser.add_argument('--end-year', type=int, help='End year for scraping')
    parser.add_argument('--bill-types', nargs='+', help='Bill types to scrape', 
                        choices=['SB', 'HB', 'SR', 'HR', 'SCR', 'HCR', 'GM'])
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between requests (seconds)')
    parser.add_argument('--max-workers', type=int, default=4, help='Number of concurrent threads (1-8)')
    parser.add_argument('--start-id', type=int, default=1, help='Start member ID')
    parser.add_argument('--end-id', type=int, default=1500, help='End member ID')
    parser.add_argument('--max-bills', type=int, default=10000, help='Maximum bill number to try')
    
    # New range-based arguments
    parser.add_argument('--member-ids', type=str, help='Member ID ranges (e.g., "1-250", "1,5,10-20")')
    parser.add_argument('--years', type=str, help='Year ranges (e.g., "2025", "2024-2025")')
    parser.add_argument('--bill-numbers', type=str, help='Bill number ranges (e.g., "1-100", "1,5,10-20")')
    
    args = parser.parse_args()
    
    # Validate max_workers
    if args.max_workers < 1 or args.max_workers > 8:
        parser.error("--max-workers must be between 1 and 8")
    
    # Initialize scraper
    scraper = BatchScraper(delay=args.delay, max_workers=args.max_workers)
    
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
    
    elif args.mode == 'range-members':
        # Parse member IDs and years from range strings
        if not args.member_ids:
            parser.error("--member-ids is required for range-members mode")
        if not args.years:
            parser.error("--years is required for range-members mode")
        
        member_ids = parse_range(args.member_ids)
        target_years = parse_year_range(args.years)
        
        scraper.scrape_members_by_range(member_ids, target_years)
    
    elif args.mode == 'range-bills':
        # Parse bill numbers, types, and years from range strings
        if not args.bill_numbers:
            parser.error("--bill-numbers is required for range-bills mode")
        if not args.years:
            parser.error("--years is required for range-bills mode")
        
        bill_numbers = parse_range(args.bill_numbers)
        target_years = parse_year_range(args.years)
        
        scraper.scrape_bills_by_range(bill_numbers, args.bill_types, target_years)
    
    elif args.mode == 'full':
        scraper.full_historical_scrape(args.start_year, args.end_year)
    
    elif args.mode == 'update':
        scraper.update_recent_data()

if __name__ == "__main__":
    main()