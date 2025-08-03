#!/usr/bin/env python3
"""
Create sample data for testing the export and frontend functionality
"""

import os
from datetime import datetime, timedelta
from database import DatabaseManager
from models import Bill, BillStatusUpdate, Member, MemberTerm

def create_sample_data():
    """Create sample data for testing"""
    # Use environment variable for database URL
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///app/data/hawaii_legislature.db')
    db_manager = DatabaseManager(database_url)
    session = db_manager.get_session()
    
    try:
        # Create database tables
        db_manager.create_tables()
        print("✓ Database tables created")
        
        # Create sample bills
        bills_data = [
            {
                'bill_type': 'SB',
                'bill_number': 1,
                'year': 2025,
                'title': 'Sample Education Funding Bill',
                'description': 'A bill to improve education funding in Hawaii',
                'current_version': 'SB1',
                'introducer': 'Sen. Sample',
                'current_referral': 'EDU',
                'current_bill_url': 'https://example.com/sb1'
            },
            {
                'bill_type': 'HB',
                'bill_number': 1,
                'year': 2025,
                'title': 'Healthcare Access Bill',
                'description': 'A bill to improve healthcare access',
                'current_version': 'HB1',
                'introducer': 'Rep. Example',
                'current_referral': 'HLT',
                'current_bill_url': 'https://example.com/hb1'
            },
            {
                'bill_type': 'SB',
                'bill_number': 100,
                'year': 2025,
                'title': 'Environmental Protection Act',
                'description': 'A bill to strengthen environmental protections',
                'current_version': 'SB100 SD1',
                'introducer': 'Sen. Green',
                'current_referral': 'ENV',
                'act_number': 25,
                'current_bill_url': 'https://example.com/sb100'
            }
        ]
        
        for bill_data in bills_data:
            bill = Bill(**bill_data)
            session.add(bill)
            session.flush()  # Get the bill ID
            
            # Add some status updates
            status_updates = [
                {
                    'bill_id': bill.id,
                    'date': datetime.now() - timedelta(days=30),
                    'chamber': 'Senate' if bill.bill_type == 'SB' else 'House',
                    'action': 'Introduced'
                },
                {
                    'bill_id': bill.id,
                    'date': datetime.now() - timedelta(days=20),
                    'chamber': 'Senate' if bill.bill_type == 'SB' else 'House',
                    'action': 'Referred to committee'
                },
                {
                    'bill_id': bill.id,
                    'date': datetime.now() - timedelta(days=10),
                    'chamber': 'Senate' if bill.bill_type == 'SB' else 'House',
                    'action': 'Committee passed'
                }
            ]
            
            if bill.act_number:
                status_updates.append({
                    'bill_id': bill.id,
                    'date': datetime.now() - timedelta(days=1),
                    'chamber': 'Governor',
                    'action': f'Signed into law as Act {bill.act_number}'
                })
            
            for status_data in status_updates:
                status_update = BillStatusUpdate(**status_data)
                session.add(status_update)
        
        print(f"✓ Created {len(bills_data)} sample bills with status updates")
        
        # Create sample members
        members_data = [
            {
                'member_id': 1,
                'name': 'Senator Jane Smith',
                'bio': 'Experienced legislator focused on education and healthcare.'
            },
            {
                'member_id': 2,
                'name': 'Representative John Doe',
                'bio': 'Community advocate working on environmental issues.'
            },
            {
                'member_id': 3,
                'name': 'Senator Maria Rodriguez',
                'bio': 'Business leader focused on economic development.'
            }
        ]
        
        for member_data in members_data:
            member = Member(**member_data)
            session.add(member)
            session.flush()
            
            # Add member term
            term_data = {
                'member_id': member.member_id,
                'year': 2025,
                'title': 'Senator' if 'Senator' in member.name else 'Representative',
                'party': 'Democratic',
                'district_type': 'Senate' if 'Senator' in member.name else 'House',
                'district_number': member.member_id,
                'district_description': f'District {member.member_id}',
                'email': f'{member.name.lower().replace(" ", ".")}@capitol.hawaii.gov',
                'phone': '(808) 555-0100',
                'photo_url': f'https://example.com/{member.name.lower().replace(" ", "_")}.jpg'
            }
            
            term = MemberTerm(**term_data)
            session.add(term)
        
        print(f"✓ Created {len(members_data)} sample members with terms")
        
        session.commit()
        print("✓ Sample data committed to database")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        session.rollback()
        raise
    finally:
        db_manager.close_session(session)

if __name__ == "__main__":
    create_sample_data()
    print("Sample data creation completed!")