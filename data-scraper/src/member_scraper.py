#!/usr/bin/env python3
"""
Comprehensive member scraping functionality for Hawaii Legislature
"""

import cloudscraper
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse
from database import DatabaseManager
from models import Member, MemberTerm, MemberCommittee
import time

class MemberScraper:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager if db_manager else DatabaseManager()
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
    
    def parse_tabbed_content(self, soup):
        """Parse tabbed content (About, Experience, News, Links)"""
        tabs_data = {}
        
        # Find tab panels
        about_panel = soup.find('div', {'role': 'tabpanel', 'aria-labelledby': lambda x: x and 'about' in x.lower()})
        if not about_panel:
            # Alternative search for About content
            about_panel = soup.find('div', id=re.compile(r'.*about.*', re.I))
        
        if about_panel:
            tabs_data['about'] = about_panel.get_text(strip=True)
        
        # Try to find experience content
        exp_panel = soup.find('div', {'role': 'tabpanel', 'aria-labelledby': lambda x: x and 'experience' in x.lower()})
        if exp_panel:
            tabs_data['experience'] = exp_panel.get_text(strip=True)
        
        # Try to find news content
        news_panel = soup.find('div', {'role': 'tabpanel', 'aria-labelledby': lambda x: x and 'news' in x.lower()})
        if news_panel:
            # Clean up news content - remove null characters and extra whitespace
            news_text = news_panel.get_text(strip=True)
            # Remove null characters and other control characters
            news_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', news_text)
            # Clean up multiple spaces and newlines
            news_text = re.sub(r'\s+', ' ', news_text).strip()
            if news_text:
                tabs_data['news'] = news_text
        
        # Try to find links content
        links_panel = soup.find('div', {'role': 'tabpanel', 'aria-labelledby': lambda x: x and 'links' in x.lower()})
        if links_panel:
            links = []
            for link in links_panel.find_all('a'):
                links.append({
                    'text': link.get_text(strip=True),
                    'url': link.get('href')
                })
            tabs_data['links'] = links
        
        return tabs_data
    
    def parse_measures_introduced(self, soup, year):
        """Parse measures/bills introduced by this member"""
        measures = []
        
        # Look for measures table
        measures_table = soup.find('table')
        if measures_table:
            rows = measures_table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    cell_content = cells[0]
                    link = cell_content.find('a')
                    if link:
                        bill_text = link.get_text(strip=True)
                        description_text = cell_content.get_text(strip=True).replace(bill_text, '').strip()
                        
                        measures.append({
                            'bill_identifier': bill_text,
                            'title': description_text,
                            'url': urljoin(self.base_url, link.get('href', ''))
                        })
        
        return measures
    
    def parse_allowance_report(self, soup, year):
        """Parse allowance report link"""
        allowance_data = {}
        
        # Look for allowance report link
        allowance_link = soup.find('a', string=re.compile(r'Expenditure Report', re.I))
        if allowance_link:
            allowance_data['allowance_report_url'] = urljoin(self.base_url, allowance_link.get('href', ''))
            allowance_data['allowance_report_text'] = allowance_link.get_text(strip=True)
        
        return allowance_data
    
    def parse_office_info(self, soup):
        """Parse office/contact information"""
        office_data = {}
        
        # Look for room information
        room_span = soup.find('span', id='MainContent_memberForm_LabelRoom')
        if not room_span:
            # Alternative search
            room_text = soup.find(string=re.compile(r'Room:'))
            if room_text:
                parent = room_text.parent
                if parent:
                    room_span = parent.find_next('span') or parent.find_next()
        
        if room_span:
            office_data['office'] = room_span.get_text(strip=True)
        
        # Look for fax information
        fax_text = soup.find(string=re.compile(r'Fax:'))
        if fax_text:
            parent = fax_text.parent
            if parent:
                fax_span = parent.find_next('span') or parent.find_next()
                if fax_span:
                    office_data['fax'] = fax_span.get_text(strip=True)
        
        return office_data
    
    def parse_committees(self, soup, year):
        """Parse committee memberships"""
        committees = []
        
        # Multiple strategies to find committee information
        
        # Strategy 1: Look for committee section by text
        committee_section = soup.find('div', string=re.compile(r'Committee Member of', re.I))
        if committee_section:
            # Find the next element which should contain the list
            committee_list = committee_section.find_next('ul')
            if committee_list:
                links = committee_list.find_all('a')
                for link in links:
                    committee_name = link.get_text(strip=True)
                    if committee_name:
                        committees.append({
                            'committee_name': committee_name,
                            'position': 'Member',  # Default position
                            'committee_type': 'Standing',  # Default type
                            'committee_url': urljoin(self.base_url, link.get('href', ''))
                        })
        
        # Strategy 2: Look for elements containing "Committee Member of"
        if not committees:
            committee_elements = soup.find_all(string=re.compile(r'Committee Member of', re.I))
            for element in committee_elements:
                parent = element.parent
                if parent:
                    # Look for lists in the parent or next siblings
                    for ul in parent.find_all('ul') + [parent.find_next('ul')]:
                        if ul:
                            links = ul.find_all('a')
                            for link in links:
                                committee_name = link.get_text(strip=True)
                                if committee_name and 'committee' in committee_name.lower():
                                    committees.append({
                                        'committee_name': committee_name,
                                        'position': 'Member',
                                        'committee_type': 'Standing',
                                        'committee_url': urljoin(self.base_url, link.get('href', ''))
                                    })
        
        # Strategy 3: Look for common committee HTML patterns
        if not committees:
            # Look for divs with class patterns that might contain committees
            for div_class in ['committee-list', 'committees', 'member-committees']:
                committee_div = soup.find('div', {'class': re.compile(div_class, re.I)})
                if committee_div:
                    links = committee_div.find_all('a')
                    for link in links:
                        committee_name = link.get_text(strip=True)
                        if committee_name:
                            committees.append({
                                'committee_name': committee_name,
                                'position': 'Member',
                                'committee_type': 'Standing',
                                'committee_url': urljoin(self.base_url, link.get('href', ''))
                            })
        
        # Strategy 4: Look for any links that might be committee links
        if not committees:
            # Find all links that contain "committee" in the URL or text
            all_links = soup.find_all('a')
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if ('committee' in href.lower() or 'committee' in text.lower()) and text:
                    # Filter out obviously non-committee links
                    if not any(word in text.lower() for word in ['home', 'back', 'legislature', 'capitol']):
                        committees.append({
                            'committee_name': text,
                            'position': 'Member',
                            'committee_type': 'Standing',
                            'committee_url': urljoin(self.base_url, href)
                        })
        
        # Remove duplicates
        seen_committees = set()
        unique_committees = []
        for committee in committees:
            if committee['committee_name'] not in seen_committees:
                seen_committees.add(committee['committee_name'])
                unique_committees.append(committee)
        
        return unique_committees
    
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
            tabs_data = self.parse_tabbed_content(soup)
            measures = self.parse_measures_introduced(soup, year)
            allowance_data = self.parse_allowance_report(soup, year)
            office_data = self.parse_office_info(soup)
            
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
                office=office_data.get('office'),
                fax=office_data.get('fax'),
                photo_url=header_data.get('photo_url'),
                rss_feed_url=header_data.get('rss_feed_url'),
                current_experience=bio_data.get('current_experience'),
                previous_experience=bio_data.get('previous_experience'),
                about_content=tabs_data.get('about'),
                experience_content=tabs_data.get('experience'),
                news_content=tabs_data.get('news'),
                links_content=json.dumps(tabs_data.get('links', [])) if tabs_data.get('links') else None,
                allowance_report_url=allowance_data.get('allowance_report_url'),
                measures_introduced=json.dumps(measures) if measures else None
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