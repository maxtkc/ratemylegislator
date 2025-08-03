#!/usr/bin/env python3
"""
Test script to verify the database schema works correctly
"""

from database import DatabaseManager
from models import (Bill, BillStatusUpdate, BillVersion, BillCommitteeReport, 
                   Member, MemberTerm, MemberCommittee)
from datetime import datetime

def test_schema():
    """Test that we can create the database and add sample data"""
    
    # Initialize database
    db_manager = DatabaseManager("sqlite:///test_hawaii_legislature.db")
    db_manager.create_tables()
    print("✓ Database tables created successfully")
    
    session = db_manager.get_session()
    
    try:
        # Test Member creation
        member = Member(
            member_id=253,
            name="Elle Cochran",
            bio="Representative Elle Cochran currently serves as the representative for House District 14."
        )
        session.add(member)
        session.flush()
        print("✓ Member created successfully")
        
        # Test MemberTerm creation
        member_term = MemberTerm(
            member_id=253,
            year=2025,
            title="Representative",
            party="D",
            district_type="House District",
            district_number=14,
            district_description="Kahakuloa, Lahaina, Olowalu, Ukumehame, Wailuku",
            email="repcochran@capitol.hawaii.gov",
            phone="808-586-6160"
        )
        session.add(member_term)
        session.flush()
        print("✓ MemberTerm created successfully")
        
        # Test MemberCommittee creation
        committee = MemberCommittee(
            member_term_id=member_term.id,
            year=2025,
            committee_name="Committee on Finance",
            position="Member"
        )
        session.add(committee)
        print("✓ MemberCommittee created successfully")
        
        # Test Bill creation
        bill = Bill(
            bill_type="SB",
            bill_number=1300,
            year=2025,
            current_version="SD1 HD1 CD1",
            title="RELATING TO SUPPLEMENTAL NUTRITION ASSISTANCE PROGRAM",
            description="Expands eligibility for SNAP benefits to persons whose household income does not exceed 200% of the federal poverty level. Appropriates funds. (CD1)",
            act_number=139,
            governor_message_number=1239
        )
        session.add(bill)
        session.flush()
        print("✓ Bill created successfully")
        
        # Test BillVersion creation
        version = BillVersion(
            bill_id=bill.id,
            version_name="SB1300_CD1",
            version_code="CD1",
            html_url="https://www.capitol.hawaii.gov/sessions/session2025/bills/SB1300_CD1_.HTM",
            pdf_url="https://www.capitol.hawaii.gov/sessions/session2025/bills/SB1300_CD1_.PDF"
        )
        session.add(version)
        print("✓ BillVersion created successfully")
        
        # Test BillStatusUpdate creation
        status_update = BillStatusUpdate(
            bill_id=bill.id,
            date=datetime(2025, 5, 30),
            chamber="H",
            action="Act 139, on 05/30/2025 (Gov. Msg. No. 1239)."
        )
        session.add(status_update)
        print("✓ BillStatusUpdate created successfully")
        
        # Test BillCommitteeReport creation
        committee_report = BillCommitteeReport(
            bill_id=bill.id,
            report_name="SB1300_SD1_SSCR96_",
            html_url="https://www.capitol.hawaii.gov/sessions/session2025/CommReports/SB1300_SD1_SSCR96_.htm",
            pdf_url="https://www.capitol.hawaii.gov/sessions/session2025/CommReports/SB1300_SD1_SSCR96_.pdf"
        )
        session.add(committee_report)
        print("✓ BillCommitteeReport created successfully")
        
        # Commit all changes
        session.commit()
        print("✓ All data committed successfully")
        
        # Test relationships
        member_from_db = session.query(Member).filter_by(member_id=253).first()
        print(f"✓ Member has {len(member_from_db.terms)} terms")
        
        bill_from_db = session.query(Bill).filter_by(bill_type="SB", bill_number=1300, year=2025).first()
        print(f"✓ Bill has {len(bill_from_db.versions)} versions")
        print(f"✓ Bill has {len(bill_from_db.status_updates)} status updates")
        print(f"✓ Bill has {len(bill_from_db.committee_reports)} committee reports")
        
        print("\n🎉 All tests passed! Database schema is working correctly.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        db_manager.close_session(session)

if __name__ == "__main__":
    test_schema()