from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (Base, Bill, BillStatusUpdate, BillVersion, BillCommitteeReport, 
                   Member, MemberTerm, MemberCommittee)
import os

class DatabaseManager:
    def __init__(self, database_url="sqlite:///hawaii_legislature.db"):
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(bind=self.engine)
        print("Database tables created successfully.")
        
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()
        
    def close_session(self, session):
        """Close a database session"""
        session.close()
        
    def bill_exists(self, session, bill_type, bill_number, year):
        """Check if a bill already exists in the database"""
        return session.query(Bill).filter_by(
            bill_type=bill_type,
            bill_number=bill_number,
            year=year
        ).first() is not None
        
    def member_exists(self, session, member_id):
        """Check if a member already exists in the database"""
        return session.query(Member).filter_by(member_id=member_id).first() is not None
        
    def member_term_exists(self, session, member_id, year):
        """Check if a member term already exists in the database"""
        return session.query(MemberTerm).filter_by(
            member_id=member_id,
            year=year
        ).first() is not None
        
    def get_or_create_member(self, session, member_id, name=None, bio=None):
        """Get existing member or create new one"""
        member = session.query(Member).filter_by(member_id=member_id).first()
        if member is None:
            member = Member(member_id=member_id, name=name, bio=bio)
            session.add(member)
            session.flush()  # Get the ID without committing
        return member
        
    def bill_version_exists(self, session, bill_id, version_name):
        """Check if a bill version already exists"""
        return session.query(BillVersion).filter_by(
            bill_id=bill_id,
            version_name=version_name
        ).first() is not None
        
    def bill_committee_report_exists(self, session, bill_id, report_name):
        """Check if a bill committee report already exists"""
        return session.query(BillCommitteeReport).filter_by(
            bill_id=bill_id,
            report_name=report_name
        ).first() is not None
        
    def member_committee_exists(self, session, member_term_id, committee_name, year):
        """Check if a member committee assignment already exists"""
        return session.query(MemberCommittee).filter_by(
            member_term_id=member_term_id,
            committee_name=committee_name,
            year=year
        ).first() is not None

def init_database():
    """Initialize the database with all tables"""
    db_manager = DatabaseManager()
    db_manager.create_tables()
    return db_manager

if __name__ == "__main__":
    # Initialize database when run directly
    init_database()
    print("Database initialized successfully!")