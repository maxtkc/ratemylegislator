#!/usr/bin/env python3
"""
Comprehensive member scraping functionality for Hawaii Legislature
"""

import cloudscraper
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from database import DatabaseManager
from models import Member, MemberTerm, MemberCommittee
import time

class MemberScraper:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.session = cloudscraper.create_scraper(
            browser={
                'browser': 'firefox',
                'platform': 'windows',
                'mobile': False
            }
        )
        self.base_url = "https://www.capitol.hawaii.gov"
    
    def fetch_member_page(self, member_id, year, max_retries=3):
        """Fetch a member page with retry logic"""
        url = f"https://www.capitol.hawaii.gov/legislature/memberpage.aspx?member={member_id}&year={year}"
        
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
    
    def parse_member_header(self, soup):
        """Parse member header information"""
        data = {}
        
        # Get member name and title
        title_span = soup.find('span', id='LabelSenRep')
        name_span = soup.find('span', id='LabelLegname')
        
        if title_span:
            data['title'] = title_span.get_text(strip=True)
        
        if name_span:
            name_and_party = name_span.get_text(strip=True)
            # Extract name and party - format is "Name (Party)"
            party_match = re.search(r'\(([^)]+)\)$', name_and_party)
            if party_match:
                data['party'] = party_match.group(1)
                data['name'] = name_and_party.replace(party_match.group(0), '').strip()
            else:
                data['name'] = name_and_party
        
        # Get photo URL
        photo_img = soup.find('img', id='memberPhoto')
        if photo_img:
            data['photo_url'] = urljoin(self.base_url, photo_img.get('src'))
        
        # Get RSS feed URL
        rss_link = soup.find('a', id='MainContent_RssFeedLink')
        if rss_link:
            data['rss_feed_url'] = urljoin(self.base_url, rss_link.get('href'))
        
        return data
    
    def parse_district_info(self, soup):
        """Parse district information"""
        data = {}
        
        # Get district link and number
        district_link = soup.find('a', id='MainContent_memberForm_HyperLinkDistrict')
        if district_link:
            district_text = district_link.get_text(strip=True)
            data['district_map_url'] = district_link.get('href')
            
            # Extract district type and number
            district_match = re.search(r'(House|Senate)\s+District\s+(\d+)', district_text, re.IGNORECASE)
            if district_match:
                data['district_type'] = f"{district_match.group(1)} District"
                data['district_number'] = int(district_match.group(2))
        
        # Get district description
        desc_span = soup.find('span', id='MainContent_memberForm_LabelDistrictDesc')
        if desc_span:
            data['district_description'] = desc_span.get_text(strip=True)
        
        return data
    
    def parse_contact_info(self, soup):
        """Parse contact information"""
        data = {}
        
        # Get phone number
        phone_span = soup.find('span', id='MainContent_memberForm_LabelPhone')
        if phone_span:
            data['phone'] = phone_span.get_text(strip=True)
        
        # Get email
        email_link = soup.find('a', id='MainContent_memberForm_HyperLinkEmail')
        if email_link:
            data['email'] = email_link.get_text(strip=True)
        
        return data
    
    def parse_biography(self, soup):
        """Parse biography and experience information"""
        data = {}
        
        # Get main biography
        bio_span = soup.find('span', id='MainContent_LabelBio')
        if bio_span:
            data['bio'] = bio_span.get_text(strip=True)
        
        # Get experience information
        exp_span = soup.find('span', id='MainContent_LabelExperience')
        if exp_span:
            # Split experience into current and previous
            exp_text = exp_span.get_text(strip=True)
            # Look for "(Present)" to identify current roles
            exp_lines = exp_text.split('<br>')
            current_exp = []
            previous_exp = []
            
            for line in exp_lines:
                line = line.strip()
                if line:
                    if '(Present)' in line:
                        current_exp.append(line)
                    else:
                        previous_exp.append(line)
            
            if current_exp:
                data['current_experience'] = '\n'.join(current_exp)
            if previous_exp:
                data['previous_experience'] = '\n'.join(previous_exp)
        
        return data
    
    def parse_committees(self, soup, year):
        """Parse committee memberships"""
        committees = []
        
        # Look for committee year label to confirm we're in the right section
        year_label = soup.find('span', id='MainContent_commYearLbl')
        if year_label and str(year) in year_label.get_text():
            # Look for committee member text
            member_text = soup.find(string=re.compile(r'Committee Member of'))
            if member_text:
                # Find the parent element and look for committee information
                parent = member_text.parent
                if parent:
                    # Look for committee listings around this area
                    # This is a simplified approach - the actual HTML structure may vary
                    committee_links = parent.find_next_siblings('a') or parent.find_all('a')
                    
                    for link in committee_links:
                        committee_name = link.get_text(strip=True)
                        if committee_name and 'committee' in committee_name.lower():
                            committees.append({
                                'committee_name': committee_name,
                                'position': 'Member',  # Default position
                                'committee_type': 'Standing'  # Default type
                            })
        
        return committees
    
    def scrape_member(self, member_id, year):
        """Scrape a single member and save to database"""
        print(f"Scraping member {member_id}-{year}")
        
        # Fetch the page
        response, url = self.fetch_member_page(member_id, year)
        if response is None:
            print(f"  Failed to fetch member {member_id}-{year}")
            return False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check if this is a valid member page
        if not soup.find('span', id='LabelLegname'):
            print(f"  No valid member content for {member_id}-{year}")
            return False
        
        db_session = self.db_manager.get_session()
        
        try:
            # Parse all member data
            header_data = self.parse_member_header(soup)
            district_data = self.parse_district_info(soup)
            contact_data = self.parse_contact_info(soup)
            bio_data = self.parse_biography(soup)
            committees = self.parse_committees(soup, year)
            
            # Check if member term already exists
            if self.db_manager.member_term_exists(db_session, member_id, year):
                print(f"  Member term {member_id}-{year} already exists")
                return True
            
            # Get or create the base member record
            member = self.db_manager.get_or_create_member(
                db_session,
                member_id,
                name=header_data.get('name'),
                bio=bio_data.get('bio')
            )
            
            # Create the member term record
            member_term = MemberTerm(
                member_id=member_id,
                year=year,
                title=header_data.get('title'),
                party=header_data.get('party'),
                district_type=district_data.get('district_type'),
                district_number=district_data.get('district_number'),
                district_description=district_data.get('district_description'),
                district_map_url=district_data.get('district_map_url'),
                email=contact_data.get('email'),
                phone=contact_data.get('phone'),
                photo_url=header_data.get('photo_url'),
                rss_feed_url=header_data.get('rss_feed_url'),
                current_experience=bio_data.get('current_experience'),
                previous_experience=bio_data.get('previous_experience')
            )
            
            db_session.add(member_term)
            db_session.flush()  # Get the member_term ID
            
            # Add committee memberships
            for committee_data in committees:
                committee = MemberCommittee(
                    member_term_id=member_term.id,
                    year=year,
                    committee_name=committee_data['committee_name'],
                    position=committee_data['position'],
                    committee_type=committee_data['committee_type']
                )
                db_session.add(committee)
            
            db_session.commit()
            print(f"  ✓ Saved member {member_id}-{year} ({header_data.get('name')}) with {len(committees)} committee assignments")
            return True
            
        except Exception as e:
            print(f"  Error saving member {member_id}-{year}: {e}")
            db_session.rollback()
            return False
        finally:
            self.db_manager.close_session(db_session)
    
    def scrape_member_range(self, year, start_id=1, end_id=1500):
        """Scrape a range of member IDs for a given year"""
        print(f"Scraping members {start_id}-{end_id} for year {year}")
        
        success_count = 0
        for member_id in range(start_id, end_id + 1):
            if self.scrape_member(member_id, year):
                success_count += 1
            
            # Progress indicator
            if member_id % 50 == 0:
                print(f"  Progress: {member_id}/{end_id} ({success_count} successful)")
            
            # Be respectful to the server
            time.sleep(0.5)
        
        print(f"Completed scraping {end_id - start_id + 1} member IDs, {success_count} successful")
        return success_count

if __name__ == "__main__":
    scraper = MemberScraper()
    
    # Test with the Member 253 example
    print("Testing member scraper with Member 253-2025...")
    scraper.scrape_member(253, 2025)
    
    # Test with a few more members
    test_members = [1, 7, 100, 200]
    
    for member_id in test_members:
        scraper.scrape_member(member_id, 2025)
        time.sleep(1)  # Be respectful to the server