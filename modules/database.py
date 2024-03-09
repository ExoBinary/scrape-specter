from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class CrawledDomains(Base):
    __tablename__ = 'crawled_domains'

    id = Column(Integer, primary_key=True)
    domain_url = Column(String, nullable=False)
    status = Column(String, nullable=False)
    createdat = Column(DateTime, default=func.current_timestamp())
    updatedat = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

class CrawledPages(Base):
    __tablename__ = 'crawled_pages'

    id = Column(Integer, primary_key=True)
    page_url = Column(Text, nullable=False)
    content = Column(Text)
    crawled_domain_id = Column(Integer, ForeignKey('crawled_domains.id'), nullable=False)
    createdat = Column(DateTime, default=func.current_timestamp())
    updatedat = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

# Update the URL below with your actual database connection string
DATABASE_URL = "postgresql://postgres:awaswe123@localhost/chatbot"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(engine)