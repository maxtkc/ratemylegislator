import cloudscraper
from bs4 import BeautifulSoup
import time
from datetime import datetime
from database import DatabaseManager
from models import (Bill, BillStatusUpdate, BillVersion, BillCommitteeReport, 
                   Member, MemberTerm, MemberCommittee)

class HawaiiLegislatureScraper:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.session = cloudscraper.create_scraper(
            browser={
                'browser': 'firefox',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        # Bill types as specified
        self.bill_types = ['SB', 'HB', 'SR', 'HR', 'SCR', 'HCR', 'GM']
        
        # Year range (2008 to current year)
        self.start_year = 2008
        self.end_year = datetime.now().year
        
    def generate_bill_url(self, bill_type, bill_number, year):
        """Generate URL for a specific bill"""
        return f"https://www.capitol.hawaii.gov/session/measure_indiv.aspx?billtype={bill_type}&billnumber={bill_number}&year={year}"
    
    def generate_member_url(self, member_id, year):
        """Generate URL for a specific member"""
        return f"https://www.capitol.hawaii.gov/legislature/memberpage.aspx?member={member_id}&year={year}"
    
    def fetch_page(self, url, max_retries=3):
        """Fetch a web page with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    return response
                elif response.status_code == 404:
                    return None
                else:
                    print(f"HTTP {response.status_code} for {url}")
                    time.sleep(2 ** attempt)
            except Exception as e:
                print(f"Request error for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        return None
    
    def scrape_bill(self, bill_type, bill_number, year):
        """Scrape a single bill (placeholder implementation)"""
        url = self.generate_bill_url(bill_type, bill_number, year)
        print(f"Scraping bill: {bill_type}{bill_number}-{year}")
        
        response = self.fetch_page(url)
        if response is None:
            return False
            
        # TODO: Implement actual parsing logic
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Placeholder: just check if we got a valid page
        if "measure_indiv_Archives" in response.text:
            print(f"  Found valid bill page for {bill_type}{bill_number}-{year}")
            return True
        
        return False
    
    def scrape_member(self, member_id, year):
        """Scrape a single member (placeholder implementation)"""
        url = self.generate_member_url(member_id, year)
        print(f"Scraping member: {member_id}-{year}")
        
        response = self.fetch_page(url)
        if response is None:
            return False
            
        # TODO: Implement actual parsing logic
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Placeholder: just check if we got a valid page
        if "memberpage" in response.text:
            print(f"  Found valid member page for {member_id}-{year}")
            
            # Placeholder for saving to database
            # This would create/update Member record and create MemberTerm record
            db_session = self.db_manager.get_session()
            try:
                # Check if this member term already exists
                if not self.db_manager.member_term_exists(db_session, member_id, year):
                    # Get or create the base member record
                    member = self.db_manager.get_or_create_member(
                        db_session, 
                        member_id,
                        name="Placeholder Name",  # TODO: Parse from page
                        bio=None  # TODO: Parse from page
                    )
                    
                    # Create the member term record
                    member_term = MemberTerm(
                        member_id=member_id,
                        year=year,
                        title="Placeholder Title",  # TODO: Parse from page
                        party="Placeholder Party",  # TODO: Parse from page
                        district_type="Placeholder District Type",  # TODO: Parse from page
                        district_number=0,  # TODO: Parse from page
                        district_description="Placeholder Description"  # TODO: Parse from page
                    )
                    db_session.add(member_term)
                    db_session.commit()
                    print(f"    Saved member term {member_id}-{year}")
                else:
                    print(f"    Member term {member_id}-{year} already exists")
            except Exception as e:
                print(f"    Error saving member {member_id}-{year}: {e}")
                db_session.rollback()
            finally:
                self.db_manager.close_session(db_session)
            
            return True
        
        return False
    
    def scrape_bills_for_year(self, year):
        """Scrape all bills for a given year"""
        print(f"Scraping bills for year {year}")
        
        for bill_type in self.bill_types:
            print(f"  Scraping {bill_type} bills for {year}")
            consecutive_404s = 0
            bill_number = 1
            
            while consecutive_404s < 2:
                success = self.scrape_bill(bill_type, bill_number, year)
                
                if success:
                    consecutive_404s = 0
                else:
                    consecutive_404s += 1
                    print(f"    404 #{consecutive_404s} for {bill_type}{bill_number}-{year}")
                
                bill_number += 1
                time.sleep(0.5)  # Be respectful to the server
                
                # Safety break to avoid infinite loops
                if bill_number > 10000:
                    print(f"    Reached safety limit for {bill_type} {year}")
                    break
    
    def scrape_members_for_year(self, year):
        """Scrape all members for a given year (1-1500 with gaps)"""
        print(f"Scraping members for year {year}")
        
        for member_id in range(1, 1501):
            success = self.scrape_member(member_id, year)
            
            if not success:
                print(f"  No member found for ID {member_id}-{year}")
            
            time.sleep(0.5)  # Be respectful to the server
            
            # Progress indicator
            if member_id % 100 == 0:
                print(f"  Processed {member_id}/1500 members for {year}")
    
    def run_full_scrape(self):
        """Run the complete scraping process"""
        print("Starting Hawaii Legislature scraper...")
        self.db_manager.create_tables()
        
        # Scrape bills for all years
        for year in range(self.start_year, self.end_year + 1):
            print(f"\n=== YEAR {year} ===")
            self.scrape_bills_for_year(year)
        
        # Scrape members for all years
        for year in range(self.start_year, self.end_year + 1):
            print(f"\n=== MEMBERS {year} ===")
            self.scrape_members_for_year(year)
        
        print("\nScraping completed!")

if __name__ == "__main__":
    scraper = HawaiiLegislatureScraper()
    
    # For testing, just try a few bills
    print("Testing bill scraping...")
    scraper.scrape_bill("SB", 1, 2015)
    scraper.scrape_bill("HB", 1, 2015)
    
    print("\nTesting member scraping...")
    scraper.scrape_member(7, 2025)
    scraper.scrape_member(1, 2025)