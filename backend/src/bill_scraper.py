#!/usr/bin/env python3
"""
Comprehensive bill scraping functionality for Hawaii Legislature
"""

import cloudscraper
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from database import DatabaseManager
from models import Bill, BillStatusUpdate, BillVersion, BillCommitteeReport
from scraper_utils import (setup_logging, clean_text, parse_date, extract_act_number, 
                          extract_governor_message_number, normalize_url, safe_get_text, 
                          safe_get_attribute)
import time
import logging

class BillScraper:
    def __init__(self, log_file="bill_scraper.log"):
        self.db_manager = DatabaseManager()
        self.session = cloudscraper.create_scraper(
            browser={
                'browser': 'firefox',
                'platform': 'windows',
                'mobile': False
            }
        )
        self.base_url = "https://www.capitol.hawaii.gov"
        self.logger = setup_logging(log_file)
    
    def fetch_bill_page(self, bill_type, bill_number, year, max_retries=3):
        """Fetch a bill page with retry logic"""
        url = f"https://www.capitol.hawaii.gov/session/measure_indiv.aspx?billtype={bill_type}&billnumber={bill_number}&year={year}"
        
        # First, visit the main page to get session cookies
        try:
            self.session.get("https://www.capitol.hawaii.gov", timeout=30)
            time.sleep(1)  # Give time for any JS to run
        except:
            pass
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    return response, url
                elif response.status_code == 404:
                    return None, url
                else:
                    print(f"HTTP {response.status_code} for {url}")
                    time.sleep(2 ** attempt)
            except Exception as e:
                print(f"Request error for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        return None, url
    
    def parse_bill_header(self, soup):
        """Parse bill header information"""
        data = {}
        
        # Get bill title/version from main header
        header_link = soup.find('a', id='MainContent_LinkButtonMeasure')
        if header_link:
            data['current_version'] = header_link.get_text(strip=True)
        
        # Get description
        desc_span = soup.find('span', id='MainContent_LabelMeasureDescription')
        if desc_span:
            data['description'] = desc_span.get_text(strip=True)
        
        # Parse metadata table
        measure_table = soup.find('table', class_='MeasureSummaryContent')
        if measure_table:
            rows = measure_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True).rstrip(':')
                    value = cells[1].get_text(strip=True)
                    
                    if 'Companion' in label:
                        data['companion'] = value
                    elif 'Package' in label:
                        data['package'] = value
                    elif 'Current Referral' in label:
                        data['current_referral'] = value
                    elif 'Introducer' in label:
                        data['introducer'] = value
        
        # Get PDF URL
        pdf_link = soup.find('a', id='MainContent_PdfLink')
        if pdf_link:
            data['current_pdf_url'] = urljoin(self.base_url, pdf_link.get('href'))
        
        return data
    
    def parse_status_updates(self, soup):
        """Parse bill status updates table"""
        status_updates = []
        
        status_table = soup.find('table', id='MainContent_GridViewStatus')
        if status_table:
            # Skip header row
            rows = status_table.find_all('tr')[1:]
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    # Parse date
                    date_text = cells[0].get_text(strip=True)
                    try:
                        date_obj = datetime.strptime(date_text, '%m/%d/%Y')
                    except ValueError:
                        continue
                    
                    # Get chamber
                    chamber = cells[1].get_text(strip=True)
                    
                    # Get action text
                    action = cells[2].get_text(strip=True)
                    
                    # Extract additional metadata from action
                    committee = None
                    conf_committee_report = None
                    meeting_info = None
                    
                    # Look for conference committee report numbers
                    conf_match = re.search(r'Conf\.?\s*Com\.?\s*Rep\.?\s*No\.?\s*(\d+)', action, re.IGNORECASE)
                    if conf_match:
                        conf_committee_report = conf_match.group(1)
                    
                    # Look for meeting information
                    if 'meeting' in action.lower():
                        meeting_info = action
                    
                    status_updates.append({
                        'date': date_obj,
                        'chamber': chamber,
                        'action': action,
                        'committee': committee,
                        'conference_committee_report_number': conf_committee_report,
                        'meeting_info': meeting_info
                    })
        
        return status_updates
    
    def parse_bill_versions(self, soup):
        """Parse bill versions section"""
        versions = []
        
        # Find the versions section
        versions_repeater = soup.find('div', id='MainContent_RepeaterVersions')
        if versions_repeater:
            version_links = versions_repeater.find_all('a', id=re.compile(r'MainContent_RepeaterVersions_VersionsLink_\d+'))
            
            for link in version_links:
                version_name = link.get_text(strip=True)
                html_url = urljoin(self.base_url, link.get('href'))
                
                # Find corresponding PDF link
                pdf_link = link.find_next('a', id=re.compile(r'MainContent_RepeaterVersions_PdfLink_\d+'))
                pdf_url = None
                if pdf_link:
                    pdf_url = urljoin(self.base_url, pdf_link.get('href'))
                
                # Extract version code (e.g., CD1, HD1, SD1)
                version_code = None
                code_match = re.search(r'_(SD\d+|HD\d+|CD\d+)$', version_name)
                if code_match:
                    version_code = code_match.group(1)
                
                versions.append({
                    'version_name': version_name,
                    'version_code': version_code,
                    'html_url': html_url,
                    'pdf_url': pdf_url
                })
        
        return versions
    
    def parse_committee_reports(self, soup):
        """Parse committee reports section"""
        reports = []
        
        # Find committee reports section
        reports_repeater = soup.find('div', id='MainContent_RepeaterCommRpt')
        if reports_repeater:
            report_links = reports_repeater.find_all('a', id=re.compile(r'MainContent_RepeaterCommRpt_CategoryLink_\d+'))
            
            for link in report_links:
                report_name = link.get_text(strip=True)
                html_url = urljoin(self.base_url, link.get('href'))
                
                # Find corresponding PDF link
                pdf_link = link.find_next('a', id=re.compile(r'MainContent_RepeaterCommRpt_PdfLink_\d+'))
                pdf_url = None
                if pdf_link:
                    pdf_url = urljoin(self.base_url, pdf_link.get('href'))
                
                reports.append({
                    'report_name': report_name,
                    'html_url': html_url,
                    'pdf_url': pdf_url
                })
        
        return reports
    
    def extract_act_info(self, status_updates):
        """Extract act number and governor message from status updates"""
        act_number = None
        gov_msg_number = None
        
        for update in status_updates:
            action = update['action']
            
            # Look for Act number
            act_match = re.search(r'Act\s+(\d+)', action, re.IGNORECASE)
            if act_match:
                act_number = int(act_match.group(1))
            
            # Look for Governor Message number
            gov_match = re.search(r'Gov\.?\s*Msg\.?\s*No\.?\s*(\d+)', action, re.IGNORECASE)
            if gov_match:
                gov_msg_number = int(gov_match.group(1))
        
        return act_number, gov_msg_number
    
    def scrape_bill(self, bill_type, bill_number, year):
        """Scrape a single bill and save to database"""
        print(f"Scraping {bill_type}{bill_number}-{year}")
        
        # Fetch the page
        response, url = self.fetch_bill_page(bill_type, bill_number, year)
        if response is None:
            print(f"  Failed to fetch {bill_type}{bill_number}-{year}")
            return False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check if this is a valid bill page
        if not soup.find('a', id='MainContent_LinkButtonMeasure'):
            print(f"  No valid bill content for {bill_type}{bill_number}-{year}")
            return False
        
        db_session = self.db_manager.get_session()
        
        try:
            # Check if bill already exists
            existing_bill = db_session.query(Bill).filter_by(
                bill_type=bill_type,
                bill_number=bill_number,
                year=year
            ).first()
            
            if existing_bill:
                print(f"  Bill {bill_type}{bill_number}-{year} already exists")
                return True
            
            # Parse all bill data
            header_data = self.parse_bill_header(soup)
            status_updates = self.parse_status_updates(soup)
            versions = self.parse_bill_versions(soup)
            committee_reports = self.parse_committee_reports(soup)
            
            # Extract act information
            act_number, gov_msg_number = self.extract_act_info(status_updates)
            
            # Create bill record
            bill = Bill(
                bill_type=bill_type,
                bill_number=bill_number,
                year=year,
                current_version=header_data.get('current_version'),
                title=header_data.get('title'),
                description=header_data.get('description'),
                introducer=header_data.get('introducer'),
                companion=header_data.get('companion'),
                package=header_data.get('package'),
                current_referral=header_data.get('current_referral'),
                act_number=act_number,
                governor_message_number=gov_msg_number,
                current_bill_url=url,
                current_pdf_url=header_data.get('current_pdf_url')
            )
            
            db_session.add(bill)
            db_session.flush()  # Get the bill ID
            
            # Add status updates
            for update_data in status_updates:
                status_update = BillStatusUpdate(
                    bill_id=bill.id,
                    date=update_data['date'],
                    chamber=update_data['chamber'],
                    action=update_data['action'],
                    committee=update_data['committee'],
                    conference_committee_report_number=update_data['conference_committee_report_number'],
                    meeting_info=update_data['meeting_info']
                )
                db_session.add(status_update)
            
            # Add versions
            for version_data in versions:
                version = BillVersion(
                    bill_id=bill.id,
                    version_name=version_data['version_name'],
                    version_code=version_data['version_code'],
                    html_url=version_data['html_url'],
                    pdf_url=version_data['pdf_url']
                )
                db_session.add(version)
            
            # Add committee reports
            for report_data in committee_reports:
                report = BillCommitteeReport(
                    bill_id=bill.id,
                    report_name=report_data['report_name'],
                    html_url=report_data['html_url'],
                    pdf_url=report_data['pdf_url']
                )
                db_session.add(report)
            
            db_session.commit()
            print(f"  ✓ Saved {bill_type}{bill_number}-{year} with {len(status_updates)} status updates, {len(versions)} versions, {len(committee_reports)} reports")
            return True
            
        except Exception as e:
            print(f"  Error saving {bill_type}{bill_number}-{year}: {e}")
            db_session.rollback()
            return False
        finally:
            self.db_manager.close_session(db_session)

if __name__ == "__main__":
    scraper = BillScraper()
    
    # Test with the SB1300 example
    print("Testing bill scraper with SB1300-2025...")
    scraper.scrape_bill("SB", 1300, 2025)
    
    # Test with a few more bills
    test_bills = [
        ("SB", 1, 2025),
        ("HB", 1, 2025),
        ("SB", 2, 2025)
    ]
    
    for bill_type, bill_number, year in test_bills:
        scraper.scrape_bill(bill_type, bill_number, year)
        time.sleep(1)  # Be respectful to the server