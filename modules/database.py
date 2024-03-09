from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Initialize dotenv to load environment variables from a .env file.
load_dotenv()

# Base class for declarative class definitions.
Base = declarative_base()

# Define the CrawledDomains model, representing the crawled_domains table in the database.
class CrawledDomains(Base):
    __tablename__ = 'crawled_domains'
    id = Column(Integer, primary_key=True)
    domain_url = Column(String, nullable=False)
    status = Column(String, nullable=False)
    createdat = Column(DateTime, default=func.current_timestamp())
    updatedat = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

# Define the CrawledPages model, representing the crawled_pages table in the database.
class CrawledPages(Base):
    __tablename__ = 'crawled_pages'
    id = Column(Integer, primary_key=True)
    page_url = Column(Text, nullable=False)
    content = Column(Text)
    crawled_domain_id = Column(Integer, ForeignKey('crawled_domains.id'), nullable=False)
    createdat = Column(DateTime, default=func.current_timestamp())
    updatedat = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

# Retrieve the DATABASE_URL environment variable.
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine, which provides a source of database connectivity and behavior.
engine = create_engine(DATABASE_URL)

# Create a sessionmaker, which is a factory for creating new Session objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Generate a database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Ensure the session is closed properly.

# Create the tables in the database using the metadata information from Base.
def create_tables():
    Base.metadata.create_all(engine)