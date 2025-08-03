#!/usr/bin/env python3
"""
Utility functions for Hawaii Legislature scraping
"""

import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
import logging

def setup_logging(log_file="hawaii_scraper.log", level=logging.INFO):
    """Set up logging configuration"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return None
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special unicode characters that might cause issues
    text = text.replace('\u00a0', ' ')  # Non-breaking space
    text = text.replace('\u2019', "'")  # Right single quotation mark
    text = text.replace('\u201c', '"')  # Left double quotation mark
    text = text.replace('\u201d', '"')  # Right double quotation mark
    
    return text.strip() if text.strip() else None

def parse_date(date_string, formats=['%m/%d/%Y', '%Y-%m-%d', '%B %d, %Y']):
    """Parse date from various string formats"""
    if not date_string:
        return None
    
    date_string = clean_text(date_string)
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    # Try to extract date from longer strings
    date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_string)
    if date_match:
        try:
            return datetime(int(date_match.group(3)), int(date_match.group(1)), int(date_match.group(2)))
        except ValueError:
            pass
    
    return None

def extract_act_number(text):
    """Extract act number from text"""
    if not text:
        return None
    
    act_match = re.search(r'Act\s+(\d+)', text, re.IGNORECASE)
    if act_match:
        return int(act_match.group(1))
    
    return None

def extract_governor_message_number(text):
    """Extract governor message number from text"""
    if not text:
        return None
    
    gov_match = re.search(r'Gov\.?\s*Msg\.?\s*No\.?\s*(\d+)', text, re.IGNORECASE)
    if gov_match:
        return int(gov_match.group(1))
    
    return None

def extract_conference_committee_report(text):
    """Extract conference committee report number from text"""
    if not text:
        return None
    
    conf_match = re.search(r'Conf\.?\s*Com\.?\s*Rep\.?\s*No\.?\s*(\d+)', text, re.IGNORECASE)
    if conf_match:
        return conf_match.group(1)
    
    return None

def parse_party_from_name(name_text):
    """Extract party affiliation from name text"""
    if not name_text:
        return None, name_text
    
    # Look for party in parentheses at the end
    party_match = re.search(r'\(([DRI])\)$', name_text)
    if party_match:
        party = party_match.group(1)
        name = name_text.replace(party_match.group(0), '').strip()
        return party, name
    
    return None, name_text

def parse_district_info(district_text):
    """Parse district information from text"""
    if not district_text:
        return None, None, None
    
    # Extract district type and number
    district_match = re.search(r'(House|Senate)\s+District\s+(\d+)', district_text, re.IGNORECASE)
    if district_match:
        district_type = f"{district_match.group(1)} District"
        district_number = int(district_match.group(2))
        return district_type, district_number, district_text
    
    return None, None, district_text

def extract_bill_version_code(version_name):
    """Extract version code from version name"""
    if not version_name:
        return None
    
    # Look for common version codes at the end
    code_match = re.search(r'_(SD\d+|HD\d+|CD\d+)$', version_name)
    if code_match:
        return code_match.group(1)
    
    return None

def normalize_url(url, base_url="https://www.capitol.hawaii.gov"):
    """Normalize and clean URLs"""
    if not url:
        return None
    
    # If it's already a full URL, return as is
    if url.startswith('http'):
        return url
    
    # If it's a relative URL, join with base
    return urljoin(base_url, url)

def extract_phone_number(text):
    """Extract and normalize phone number from text"""
    if not text:
        return None
    
    # Look for phone number patterns
    phone_match = re.search(r'(\d{3}[-.]?\d{3}[-.]?\d{4})', text)
    if phone_match:
        # Normalize to XXX-XXX-XXXX format
        phone = re.sub(r'\D', '', phone_match.group(1))
        if len(phone) == 10:
            return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    
    return text

def extract_email(text):
    """Extract email address from text"""
    if not text:
        return None
    
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        return email_match.group(0).lower()
    
    return None

def parse_committee_position(text):
    """Parse committee position from text"""
    if not text:
        return "Member"
    
    text_lower = text.lower()
    
    if 'chair' in text_lower and 'vice' not in text_lower:
        return "Chair"
    elif 'vice' in text_lower and 'chair' in text_lower:
        return "Vice Chair"
    elif 'member' in text_lower:
        return "Member"
    
    return "Member"  # Default

def validate_bill_type(bill_type):
    """Validate and normalize bill type"""
    valid_types = ['SB', 'HB', 'SR', 'HR', 'SCR', 'HCR', 'GM']
    
    if not bill_type:
        return None
    
    bill_type = bill_type.upper().strip()
    
    if bill_type in valid_types:
        return bill_type
    
    return None

def validate_year(year):
    """Validate year is within reasonable range"""
    if not year:
        return None
    
    try:
        year_int = int(year)
        if 2008 <= year_int <= datetime.now().year + 1:
            return year_int
    except (ValueError, TypeError):
        pass
    
    return None

def extract_numeric_id(text):
    """Extract numeric ID from text"""
    if not text:
        return None
    
    # Extract first number found
    number_match = re.search(r'\d+', str(text))
    if number_match:
        try:
            return int(number_match.group(0))
        except ValueError:
            pass
    
    return None

def safe_get_text(element, default=""):
    """Safely get text from BeautifulSoup element"""
    if element is None:
        return default
    
    try:
        text = element.get_text(strip=True)
        return clean_text(text) or default
    except Exception:
        return default

def safe_get_attribute(element, attribute, default=""):
    """Safely get attribute from BeautifulSoup element"""
    if element is None:
        return default
    
    try:
        value = element.get(attribute)
        return value if value is not None else default
    except Exception:
        return default

class ScrapingStats:
    """Track scraping statistics"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.total_attempted = 0
        self.total_successful = 0
        self.total_failed = 0
        self.total_skipped = 0
        self.start_time = datetime.now()
    
    def record_attempt(self):
        self.total_attempted += 1
    
    def record_success(self):
        self.total_successful += 1
    
    def record_failure(self):
        self.total_failed += 1
    
    def record_skip(self):
        self.total_skipped += 1
    
    def get_summary(self):
        elapsed = datetime.now() - self.start_time
        return {
            'attempted': self.total_attempted,
            'successful': self.total_successful,
            'failed': self.total_failed,
            'skipped': self.total_skipped,
            'success_rate': self.total_successful / max(self.total_attempted, 1) * 100,
            'elapsed_time': str(elapsed),
            'avg_time_per_item': elapsed.total_seconds() / max(self.total_attempted, 1)
        }
    
    def print_summary(self):
        summary = self.get_summary()
        print(f"\n--- Scraping Summary ---")
        print(f"Total attempted: {summary['attempted']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Skipped: {summary['skipped']}")
        print(f"Success rate: {summary['success_rate']:.1f}%")
        print(f"Elapsed time: {summary['elapsed_time']}")
        print(f"Average time per item: {summary['avg_time_per_item']:.2f}s")

if __name__ == "__main__":
    # Test utility functions
    print("Testing utility functions...")
    
    # Test date parsing
    test_dates = ["4/25/2025", "2025-04-25", "April 25, 2025"]
    for date_str in test_dates:
        parsed = parse_date(date_str)
        print(f"Date '{date_str}' -> {parsed}")
    
    # Test text cleaning
    dirty_text = "  This is\u00a0some  \n\n dirty\u2019text  "
    clean = clean_text(dirty_text)
    print(f"Clean text: '{clean}'")
    
    # Test party parsing
    name_with_party = "Elle Cochran (D)"
    party, name = parse_party_from_name(name_with_party)
    print(f"Name: '{name}', Party: '{party}'")
    
    # Test stats tracking
    stats = ScrapingStats()
    stats.record_attempt()
    stats.record_success()
    stats.print_summary()