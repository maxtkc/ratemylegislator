#!/usr/bin/env python3
"""
Data export functionality for generating static JSON files for the frontend
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from database import DatabaseManager
from models import Bill, Member, BillStatusUpdate, MemberTerm, MemberCommittee
from sqlalchemy import func, desc

class DataExporter:
    def __init__(self, output_dir=None, db_manager=None):
        if db_manager:
            self.db_manager = db_manager
        else:
            # Use environment variable for database URL
            database_url = os.environ.get('DATABASE_URL', 'sqlite:///app/data/hawaii_legislature.db')
            self.db_manager = DatabaseManager(database_url)
            # Ensure tables exist
            self.db_manager.create_tables()
        
        # Use environment variable or default to the mounted volume
        if output_dir is None:
            output_dir = os.environ.get('EXPORT_DIR', '/app/export')
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_all_data(self):
        """Export all data for static site generation"""
        print("Starting data export for static site generation...")
        
        # Export summary statistics
        self.export_summary_stats()
        
        # Export bills data
        self.export_bills()
        
        # Export members data
        self.export_members()
        
        # Export recent activity
        self.export_recent_activity()
        
        # Export bill types and status counts
        self.export_bill_analytics()
        
        print(f"✓ Data export completed. Files saved to {self.output_dir}")
    
    def export_summary_stats(self):
        """Export overall summary statistics"""
        session = self.db_manager.get_session()
        
        try:
            stats = {
                "last_updated": datetime.now().isoformat(),
                "total_bills": session.query(Bill).count(),
                "total_members": session.query(Member).count(),
                "years_available": [row[0] for row in session.query(Bill.year.distinct()).order_by(Bill.year.desc()).all()],
                "bill_types": [row[0] for row in session.query(Bill.bill_type.distinct()).order_by(Bill.bill_type).all()]
            }
            
            self._write_json_file("summary.json", stats)
            
        finally:
            self.db_manager.close_session(session)
    
    def export_bills(self):
        """Export bills data with pagination for performance"""
        session = self.db_manager.get_session()
        
        try:
            # Export bills by year for better organization
            years = session.query(Bill.year.distinct()).order_by(Bill.year.desc()).all()
            
            for year_tuple in years:
                year = year_tuple[0]
                bills_query = session.query(Bill).filter_by(year=year).order_by(Bill.bill_type, Bill.bill_number)
                
                bills_data = []
                for bill in bills_query.all():
                    # Get latest status update
                    latest_status = session.query(BillStatusUpdate).filter_by(bill_id=bill.id).order_by(desc(BillStatusUpdate.date)).first()
                    
                    bill_data = {
                        "id": bill.id,
                        "bill_type": bill.bill_type,
                        "bill_number": bill.bill_number,
                        "year": bill.year,
                        "title": bill.title,
                        "description": bill.description,
                        "current_version": bill.current_version,
                        "introducer": bill.introducer,
                        "companion": bill.companion,
                        "current_referral": bill.current_referral,
                        "act_number": bill.act_number,
                        "governor_message_number": bill.governor_message_number,
                        "current_bill_url": bill.current_bill_url,
                        "current_pdf_url": bill.current_pdf_url,
                        "status_count": session.query(BillStatusUpdate).filter_by(bill_id=bill.id).count(),
                        "latest_status": {
                            "date": latest_status.date.isoformat() if latest_status else None,
                            "chamber": latest_status.chamber if latest_status else None,
                            "action": latest_status.action if latest_status else None
                        } if latest_status else None
                    }
                    bills_data.append(bill_data)
                
                self._write_json_file(f"bills_{year}.json", bills_data)
            
            # Export all bills summary (lighter version)
            all_bills_query = session.query(Bill).order_by(desc(Bill.year), Bill.bill_type, Bill.bill_number)
            all_bills_summary = []
            
            for bill in all_bills_query.all():
                all_bills_summary.append({
                    "id": bill.id,
                    "bill_type": bill.bill_type,
                    "bill_number": bill.bill_number,
                    "year": bill.year,
                    "title": bill.title,
                    "current_version": bill.current_version,
                    "act_number": bill.act_number
                })
            
            self._write_json_file("bills_all.json", all_bills_summary)
            
        finally:
            self.db_manager.close_session(session)
    
    def export_members(self):
        """Export members data"""
        session = self.db_manager.get_session()
        
        try:
            members_data = []
            
            for member in session.query(Member).order_by(Member.name).all():
                # Get most recent term info
                latest_term = session.query(MemberTerm).filter_by(member_id=member.member_id).order_by(desc(MemberTerm.year)).first()
                
                # Get committee assignments
                committees = []
                if latest_term:
                    committee_assignments = session.query(MemberCommittee).filter_by(member_term_id=latest_term.id).all()
                    committees = [{
                        "committee_name": assignment.committee_name,
                        "position": assignment.position,
                        "committee_type": assignment.committee_type
                    } for assignment in committee_assignments]
                
                # Parse JSON fields
                measures_introduced = []
                links = []
                if latest_term:
                    if latest_term.measures_introduced:
                        try:
                            measures_introduced = json.loads(latest_term.measures_introduced)
                        except (json.JSONDecodeError, TypeError):
                            measures_introduced = []
                    
                    if latest_term.links_content:
                        try:
                            links = json.loads(latest_term.links_content)
                        except (json.JSONDecodeError, TypeError):
                            links = []
                
                member_data = {
                    "id": member.id,
                    "member_id": member.member_id,
                    "name": member.name,
                    "bio": member.bio,
                    "latest_term": {
                        "year": latest_term.year if latest_term else None,
                        "title": latest_term.title if latest_term else None,
                        "party": latest_term.party if latest_term else None,
                        "district_type": latest_term.district_type if latest_term else None,
                        "district_number": latest_term.district_number if latest_term else None,
                        "district_description": latest_term.district_description if latest_term else None,
                        "district_map_url": latest_term.district_map_url if latest_term else None,
                        "email": latest_term.email if latest_term else None,
                        "phone": latest_term.phone if latest_term else None,
                        "office": latest_term.office if latest_term else None,
                        "fax": latest_term.fax if latest_term else None,
                        "current_experience": latest_term.current_experience if latest_term else None,
                        "previous_experience": latest_term.previous_experience if latest_term else None,
                        "about_content": latest_term.about_content if latest_term else None,
                        "experience_content": latest_term.experience_content if latest_term else None,
                        "news_content": latest_term.news_content if latest_term else None,
                        "allowance_report_url": latest_term.allowance_report_url if latest_term else None,
                        "rss_feed_url": latest_term.rss_feed_url if latest_term else None
                    } if latest_term else None,
                    "committees": committees,
                    "measures_introduced": measures_introduced,
                    "links": links,
                    "photo_url": latest_term.photo_url if latest_term else None
                }
                members_data.append(member_data)
            
            self._write_json_file("members.json", members_data)
            
        finally:
            self.db_manager.close_session(session)
    
    def export_recent_activity(self):
        """Export recent legislative activity"""
        session = self.db_manager.get_session()
        
        try:
            # Get recent status updates (last 30 days or last 50 updates)
            recent_updates = session.query(BillStatusUpdate).join(Bill).order_by(desc(BillStatusUpdate.date)).limit(50).all()
            
            activity_data = []
            for update in recent_updates:
                activity_data.append({
                    "date": update.date.isoformat(),
                    "bill_id": update.bill_id,
                    "bill_identifier": f"{update.bill.bill_type}{update.bill.bill_number}-{update.bill.year}",
                    "bill_title": update.bill.title,
                    "chamber": update.chamber,
                    "action": update.action
                })
            
            self._write_json_file("recent_activity.json", activity_data)
            
        finally:
            self.db_manager.close_session(session)
    
    def export_bill_analytics(self):
        """Export analytics data for charts and visualizations"""
        session = self.db_manager.get_session()
        
        try:
            # Bills by type
            bills_by_type = {}
            type_counts = session.query(Bill.bill_type, func.count(Bill.id)).group_by(Bill.bill_type).all()
            for bill_type, count in type_counts:
                bills_by_type[bill_type] = count
            
            # Bills by year
            bills_by_year = {}
            year_counts = session.query(Bill.year, func.count(Bill.id)).group_by(Bill.year).order_by(Bill.year).all()
            for year, count in year_counts:
                bills_by_year[str(year)] = count
            
            # Bills with acts (passed bills)
            passed_bills = session.query(Bill).filter(Bill.act_number.isnot(None)).count()
            total_bills = session.query(Bill).count()
            
            analytics_data = {
                "bills_by_type": bills_by_type,
                "bills_by_year": bills_by_year,
                "passage_rate": {
                    "passed": passed_bills,
                    "total": total_bills,
                    "percentage": round((passed_bills / total_bills * 100), 2) if total_bills > 0 else 0
                }
            }
            
            self._write_json_file("analytics.json", analytics_data)
            
        finally:
            self.db_manager.close_session(session)
    
    def _write_json_file(self, filename: str, data: Any):
        """Write data to JSON file with proper formatting"""
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"  ✓ Exported {filepath}")

def main():
    """Main function for running data export"""
    exporter = DataExporter()
    exporter.export_all_data()

if __name__ == "__main__":
    main()