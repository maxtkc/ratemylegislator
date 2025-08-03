#!/usr/bin/env python3
"""
Limited scraper for 10 bills and 10 legislators from 2025
"""

from batch_scraper import BatchScraper

def main():
    print("Starting limited scrape: 10 bills + 10 legislators for 2025")
    
    scraper = BatchScraper(delay=1.0)  # 1 second delay to be respectful
    
    # Define 10 bills to scrape (mix of SB and HB, starting from 1)
    bills_to_scrape = [
        ("SB", 1, 2025),
        ("SB", 2, 2025), 
        ("SB", 3, 2025),
        ("SB", 4, 2025),
        ("SB", 5, 2025),
        ("HB", 1, 2025),
        ("HB", 2, 2025),
        ("HB", 3, 2025),
        ("HB", 4, 2025),
        ("HB", 5, 2025)
    ]
    
    # Define 10 member IDs to scrape
    members_to_scrape = [
        (1, 2025),
        (7, 2025),
        (12, 2025),
        (25, 2025),
        (50, 2025),
        (100, 2025),
        (150, 2025),
        (200, 2025),
        (250, 2025),
        (253, 2025)  # We know this one exists from previous tests
    ]
    
    print("\n=== SCRAPING 10 BILLS ===")
    scraper.scrape_specific_bills(bills_to_scrape)
    
    print("\n=== SCRAPING 10 LEGISLATORS ===")
    scraper.scrape_specific_members(members_to_scrape)
    
    print("\n✓ Limited scrape completed!")
    print("Scraped 10 bills and 10 legislators for 2025")

if __name__ == "__main__":
    main()