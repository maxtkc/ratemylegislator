from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, unique=True, nullable=False)  # Hawaii's member ID
    name = Column(String(255))
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to member terms
    terms = relationship("MemberTerm", back_populates="member", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Member({self.member_id}, {self.name})>"

class MemberTerm(Base):
    __tablename__ = 'member_terms'
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('members.member_id'), nullable=False)
    year = Column(Integer, nullable=False)
    
    # Basic info
    title = Column(String(255))  # e.g., "Senator", "Representative"
    party = Column(String(50))   # e.g., "D", "R", "I"
    
    # District information
    district_type = Column(String(50))  # "House District", "Senate District"
    district_number = Column(Integer)
    district_description = Column(Text)  # Geographic description
    district_map_url = Column(String(500))
    
    # Contact information
    email = Column(String(255))
    phone = Column(String(50))
    office = Column(String(255))
    
    # URLs and media
    photo_url = Column(String(500))
    rss_feed_url = Column(String(500))
    
    # Professional background
    current_experience = Column(Text)  # Current roles and positions
    previous_experience = Column(Text)  # Previous roles and experience
    
    # Additional contact information
    fax = Column(String(50))
    
    # Tab content from member page
    about_content = Column(Text)
    experience_content = Column(Text)
    news_content = Column(Text)
    links_content = Column(Text)  # JSON string of links
    
    # Reports and measures
    allowance_report_url = Column(String(500))
    measures_introduced = Column(Text)  # JSON string of measures
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    member = relationship("Member", back_populates="terms")
    committee_memberships = relationship("MemberCommittee", back_populates="member_term", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MemberTerm({self.member_id}, {self.year}, {self.title})>"

class MemberCommittee(Base):
    __tablename__ = 'member_committees'
    
    id = Column(Integer, primary_key=True)
    member_term_id = Column(Integer, ForeignKey('member_terms.id'), nullable=False)
    year = Column(Integer, nullable=False)
    
    # Committee information
    committee_name = Column(String(255), nullable=False)
    position = Column(String(100))  # "Chair", "Vice Chair", "Member"
    committee_type = Column(String(50))  # "Standing", "Select", "Joint", etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship back to member term
    member_term = relationship("MemberTerm", back_populates="committee_memberships")
    
    def __repr__(self):
        return f"<MemberCommittee({self.committee_name}, {self.position})>"

class Bill(Base):
    __tablename__ = 'bills'
    
    id = Column(Integer, primary_key=True)
    bill_type = Column(String(10), nullable=False)  # SB, HB, SR, HR, SCR, HCR, GM
    bill_number = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    # Bill identification and versions
    current_version = Column(String(50))  # e.g., "SD1 HD1 CD1"
    title = Column(String(500))
    description = Column(Text)
    
    # Bill metadata
    introducer = Column(Text)  # Can be multiple introducers
    companion = Column(String(100))
    package = Column(String(100))
    current_referral = Column(String(500))
    
    # Final status
    act_number = Column(Integer)  # If signed into law
    governor_message_number = Column(Integer)  # Gov. Msg. No.
    
    # URLs
    current_bill_url = Column(String(500))
    current_pdf_url = Column(String(500))
    rss_feed_url = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    status_updates = relationship("BillStatusUpdate", back_populates="bill", cascade="all, delete-orphan")
    versions = relationship("BillVersion", back_populates="bill", cascade="all, delete-orphan")
    committee_reports = relationship("BillCommitteeReport", back_populates="bill", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Bill({self.bill_type}{self.bill_number}-{self.year})>"

class BillStatusUpdate(Base):
    __tablename__ = 'bill_status_updates'
    
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey('bills.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    chamber = Column(String(1))  # 'H' for House, 'S' for Senate
    action = Column(Text, nullable=False)
    
    # Additional metadata that might be extracted
    committee = Column(String(255))
    conference_committee_report_number = Column(String(50))
    meeting_info = Column(Text)  # For scheduled meetings
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship back to bill
    bill = relationship("Bill", back_populates="status_updates")
    
    def __repr__(self):
        return f"<BillStatusUpdate({self.bill_id}, {self.date}, {self.action[:50]})>"

class BillVersion(Base):
    __tablename__ = 'bill_versions'
    
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey('bills.id'), nullable=False)
    version_name = Column(String(50), nullable=False)  # e.g., "SB1300_CD1", "SB1300_HD1"
    version_code = Column(String(20))  # e.g., "CD1", "HD1", "SD1"
    
    # URLs
    html_url = Column(String(500))
    pdf_url = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship back to bill
    bill = relationship("Bill", back_populates="versions")
    
    def __repr__(self):
        return f"<BillVersion({self.version_name})>"

class BillCommitteeReport(Base):
    __tablename__ = 'bill_committee_reports'
    
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey('bills.id'), nullable=False)
    report_name = Column(String(100), nullable=False)  # e.g., "SB1300_SD1_SSCR96_"
    
    # URLs
    html_url = Column(String(500))
    pdf_url = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship back to bill
    bill = relationship("Bill", back_populates="committee_reports")
    
    def __repr__(self):
        return f"<BillCommitteeReport({self.report_name})>"

# Database setup functions
def create_database(database_url="sqlite:///hawaii_legislature.db"):
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()