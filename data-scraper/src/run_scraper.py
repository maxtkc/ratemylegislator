#!/usr/bin/env python3
"""
Simple script to run Hawaii Legislature scrapers
"""

import argparse
import sys
from datetime import datetime
from bill_scraper import BillScraper
from member_scraper import MemberScraper
from batch_scraper import BatchScraper
from database import DatabaseManager

def run_quick_test():
    """Run a quick test of the scrapers"""
    print("Running quick test of scrapers...")
    
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.create_tables()
    print("✓ Database initialized")
    
    # Test bill scraper
    print("\nTesting bill scraper...")
    bill_scraper = BillScraper()
    success = bill_scraper.scrape_bill("SB", 1300, 2025)
    if success:
        print("✓ Bill scraper working")
    else:
        print("❌ Bill scraper failed")
    
    # Test member scraper
    print("\nTesting member scraper...")
    member_scraper = MemberScraper()
    success = member_scraper.scrape_member(253, 2025)
    if success:
        print("✓ Member scraper working")
    else:
        print("❌ Member scraper failed")
    
    print("\n🎉 Quick test completed!")

def run_sample_scrape():
    """Run a sample scrape of recent data"""
    print("Running sample scrape...")
    
    batch_scraper = BatchScraper(delay=1.0)  # Be extra respectful during testing
    
    # Scrape a few bills from 2025
    sample_bills = [
        ("SB", 1, 2025),
        ("SB", 2, 2025),
        ("HB", 1, 2025),
        ("SB", 1300, 2025)
    ]
    
    print(f"Scraping {len(sample_bills)} sample bills...")
    batch_scraper.scrape_specific_bills(sample_bills)
    
    # Scrape a few members from 2025
    sample_members = [
        (1, 2025),
        (7, 2025),
        (253, 2025),
        (100, 2025)
    ]
    
    print(f"Scraping {len(sample_members)} sample members...")
    batch_scraper.scrape_specific_members(sample_members)
    
    print("✓ Sample scrape completed!")

def show_usage():
    """Show usage examples"""
    print("""
Hawaii Legislature Scraper Usage Examples:

1. Quick Test:
   python run_scraper.py --test

2. Sample Scrape:
   python run_scraper.py --sample

3. Scrape all bills for 2025:
   python batch_scraper.py --mode bills --year 2025

4. Scrape all members for 2025:
   python batch_scraper.py --mode members --year 2025

5. Scrape both bills and members for 2024-2025:
   python batch_scraper.py --mode both --start-year 2024 --end-year 2025

6. Full historical scrape (2008-present):
   python batch_scraper.py --mode full

7. Update recent data only:
   python batch_scraper.py --mode update

8. Scrape specific bill types only:
   python batch_scraper.py --mode bills --year 2025 --bill-types SB HB

9. Test with slower requests:
   python batch_scraper.py --mode test --delay 2.0

For more options, run:
   python batch_scraper.py --help
""")

def check_database():
    """Check database status and show some statistics"""
    print("Checking database status...")
    
    db_manager = DatabaseManager()
    session = db_manager.get_session()
    
    try:
        from models import Bill, Member, MemberTerm, BillStatusUpdate
        
        # Count records
        bill_count = session.query(Bill).count()
        member_count = session.query(Member).count()
        member_term_count = session.query(MemberTerm).count()
        status_update_count = session.query(BillStatusUpdate).count()
        
        print(f"Database Statistics:")
        print(f"  Bills: {bill_count}")
        print(f"  Members: {member_count}")
        print(f"  Member Terms: {member_term_count}")
        print(f"  Bill Status Updates: {status_update_count}")
        
        # Show recent bills
        if bill_count > 0:
            recent_bills = session.query(Bill).order_by(Bill.created_at.desc()).limit(5).all()
            print(f"\nRecent Bills:")
            for bill in recent_bills:
                print(f"  {bill.bill_type}{bill.bill_number}-{bill.year}: {bill.description[:100] if bill.description else 'No description'}...")
        
        # Show recent members
        if member_term_count > 0:
            recent_members = session.query(MemberTerm).order_by(MemberTerm.created_at.desc()).limit(5).all()
            print(f"\nRecent Member Terms:")
            for term in recent_members:
                member = term.member
                print(f"  {term.title} {member.name} ({term.party}) - {term.district_type} {term.district_number}, {term.year}")
    
    except Exception as e:
        print(f"Error checking database: {e}")
    
    finally:
        db_manager.close_session(session)

def main():
    parser = argparse.ArgumentParser(description='Hawaii Legislature Scraper Runner')
    parser.add_argument('--test', action='store_true', help='Run quick test')
    parser.add_argument('--sample', action='store_true', help='Run sample scrape')
    parser.add_argument('--usage', action='store_true', help='Show usage examples')
    parser.add_argument('--check-db', action='store_true', help='Check database status')
    parser.add_argument('--init-db', action='store_true', help='Initialize database')
    
    args = parser.parse_args()
    
    if args.init_db:
        print("Initializing database...")
        db_manager = DatabaseManager()
        db_manager.create_tables()
        print("✓ Database initialized!")
        return
    
    if args.test:
        run_quick_test()
        return
    
    if args.sample:
        run_sample_scrape()
        return
    
    if args.usage:
        show_usage()
        return
    
    if args.check_db:
        check_database()
        return
    
    # Default: show help
    parser.print_help()
    print("\nFor detailed scraping options, use batch_scraper.py")

if __name__ == "__main__":
    main()