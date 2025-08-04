#!/usr/bin/env python3
"""
Test script for enhanced member data scraping functionality
"""

from batch_scraper import BatchScraper
from data_exporter import DataExporter
import json

def main():
    print("🧪 Testing Enhanced Member Data Scraping")
    print("=" * 50)
    
    # Create batch scraper with shared database manager
    scraper = BatchScraper(delay=1.0)
    
    print("📋 Step 1: Scraping sample data...")
    # Test with specific member 253 (Elle Cochran) who we know has rich data
    test_members = [(253, 2025)]
    scraper.scrape_specific_members(test_members)
    
    test_bills = [("SB", 1, 2025), ("HB", 1, 2025)]
    scraper.scrape_specific_bills(test_bills)
    
    print("\n📤 Step 2: Exporting enhanced member data...")
    # Create data exporter using the same database manager
    exporter = DataExporter(db_manager=scraper.db_manager)
    exporter.export_all_data()
    
    # Check if the export worked by examining the members.json
    try:
        with open('/app/export/members.json', 'r') as f:
            members_data = json.load(f)
            
        print(f"\n✅ Export Results:")
        print(f"   📊 Total members exported: {len(members_data)}")
        
        if members_data:
            member = members_data[0]
            latest_term = member.get('latest_term', {})
            
            print(f"   👤 Sample member: {member.get('name', 'Unknown')}")
            print(f"   📧 Email: {latest_term.get('email', 'N/A')}")
            print(f"   📞 Phone: {latest_term.get('phone', 'N/A')}")
            print(f"   🏢 Office: {latest_term.get('office', 'N/A')}")
            print(f"   📠 Fax: {latest_term.get('fax', 'N/A')}")
            print(f"   📋 Committees: {len(member.get('committees', []))}")
            print(f"   🏛️ Measures introduced: {len(member.get('measures_introduced', []))}")
            print(f"   🔗 Links: {len(member.get('links', []))}")
            print(f"   📝 About content: {'✓' if latest_term.get('about_content') else '✗'}")
            print(f"   💼 Experience content: {'✓' if latest_term.get('experience_content') else '✗'}")
            print(f"   📰 News content: {'✓' if latest_term.get('news_content') else '✗'}")
            print(f"   💰 Allowance report: {'✓' if latest_term.get('allowance_report_url') else '✗'}")
            
            print(f"\n🔍 Enhanced Data Fields Available:")
            enhanced_fields = [
                'office', 'fax', 'about_content', 'experience_content', 
                'news_content', 'allowance_report_url'
            ]
            for field in enhanced_fields:
                status = "✅" if latest_term.get(field) else "⚠️ "
                print(f"   {status} {field}")
                
        print(f"\n🎉 Enhanced member data scraping test completed!")
        
    except FileNotFoundError:
        print("❌ Export file not found")
    except Exception as e:
        print(f"❌ Error reading export: {e}")

if __name__ == "__main__":
    main()