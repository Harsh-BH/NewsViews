from typing import List, Dict, Optional, Any
import datetime
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import sqlite3
from config import settings
from models.news import ProcessedSubmission

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SQLAlchemy
Base = declarative_base()

class SubmissionRecord(Base):
    """Database model for news submissions"""
    __tablename__ = "submissions"
    
    id = Column(String(36), primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    news_title = Column(String(200), nullable=False)
    news_description = Column(Text, nullable=False)
    city = Column(String(100))
    category = Column(String(50))
    publisher_name = Column(String(100))
    publisher_phone = Column(String(20))
    image_path = Column(String(500))
    status = Column(String(20), default="pending")
    duplicate_of = Column(String(36), nullable=True)
    
    def to_model(self) -> ProcessedSubmission:
        """Convert database record to ProcessedSubmission model"""
        return ProcessedSubmission(
            id=self.id,
            timestamp=self.timestamp,
            news_title=self.news_title,
            news_description=self.news_description,
            city=self.city,
            category=self.category,
            publisher_name=self.publisher_name,
            publisher_phone=self.publisher_phone,
            image_path=self.image_path,
            status=self.status
        )


class DatabaseService:
    """Service for database operations"""
    
    def __init__(self):
        """Initialize the database service with connection from settings"""
        try:
            # Get database URL from settings
            database_url = settings.DATABASE_URL
            logger.info(f"Connecting to database: {database_url.replace(settings.DATABASE_PASSWORD, '********')}")
            
            # Create engine
            self.engine = create_engine(database_url)
            
            # Create session factory
            self.Session = sessionmaker(bind=self.engine)
            
            # Create tables if they don't exist
            Base.metadata.create_all(self.engine)
            logger.info("Database connection established and tables created")
            
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
    
    def get_session(self):
        """Get a new session"""
        return self.Session()
    
    def get_all_submissions(self) -> List[ProcessedSubmission]:
        """Get all submissions from database"""
        try:
            with self.get_session() as session:
                records = session.query(SubmissionRecord).all()
                return [record.to_model() for record in records]
        except Exception as e:
            logger.error(f"Error getting all submissions: {str(e)}")
            raise
    
    def get_submission_by_id(self, submission_id: str) -> Optional[ProcessedSubmission]:
        """Get a specific submission by ID"""
        try:
            with self.get_session() as session:
                record = session.query(SubmissionRecord).filter(
                    SubmissionRecord.id == submission_id
                ).first()
                
                if record:
                    return record.to_model()
                return None
        except Exception as e:
            logger.error(f"Error getting submission by ID: {str(e)}")
            raise
    
    def add_submission(self, submission: ProcessedSubmission):
        """Add a new submission to the database"""
        try:
            with self.get_session() as session:
                record = SubmissionRecord(
                    id=submission.id,
                    timestamp=submission.timestamp,
                    news_title=submission.news_title,
                    news_description=submission.news_description,
                    city=submission.city,
                    category=submission.category,
                    publisher_name=submission.publisher_name,
                    publisher_phone=submission.publisher_phone,
                    image_path=submission.image_path,
                    status=submission.status
                )
                
                session.add(record)
                session.commit()
                logger.info(f"Saved submission: {record.id}")
        except Exception as e:
            logger.error(f"Error adding submission: {str(e)}")
            raise
    
    def save_submission(self, submission: ProcessedSubmission):
        """
        Save a submission to the database (compatibility method that calls add_submission)
        Note: This method is maintained for backward compatibility with existing code
        """
        try:
            logger.info(f"Saving submission to database: {submission.id}")
            # Simply call add_submission method that has the actual implementation
            self.add_submission(submission)
        except Exception as e:
            logger.error(f"Error in save_submission: {str(e)}")
            raise
    
    def update_submission_status(
        self, submission_id: str, status: str, duplicate_of: str = None
    ) -> bool:
        """Update the status of a submission"""
        try:
            with self.get_session() as session:
                record = session.query(SubmissionRecord).filter(
                    SubmissionRecord.id == submission_id
                ).first()
                
                if not record:
                    return False
                    
                record.status = status
                if duplicate_of:
                    record.duplicate_of = duplicate_of
                    
                session.commit()
                logger.info(f"Updated submission status: {record.id}")
                return True
        except Exception as e:
            logger.error(f"Error updating submission status: {str(e)}")
            raise

    def get_submissions(self, filters: Dict[str, Any] = None, limit: int = 10, offset: int = 0) -> List[Dict]:
        """
        Get news submissions with optional filters and pagination
        
        Args:
            filters: Dictionary of filter conditions
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of news submissions as dictionaries
        """
        try:
            with self.get_session() as session:
                query = session.query(SubmissionRecord)
                
                # Apply filters if provided
                if filters and len(filters) > 0:
                    for key, value in filters.items():
                        if value is not None and hasattr(SubmissionRecord, key):
                            query = query.filter(getattr(SubmissionRecord, key) == value)
                
                # Add ordering and pagination
                query = query.order_by(SubmissionRecord.timestamp.desc()).limit(limit).offset(offset)
                
                records = query.all()
                # Convert records to dictionaries
                result = []
                for record in records:
                    submission = record.to_model()
                    # Convert to dict and map field names to match expected API format
                    submission_dict = {
                        "id": submission.id,
                        "title": submission.news_title,
                        "description": submission.news_description,
                        "city": submission.city,
                        "category": submission.category,
                        "reporter_name": submission.publisher_name,
                        "contact_number": submission.publisher_phone,
                        "image_url": submission.image_path,
                        "status": submission.status,
                        "created_at": submission.timestamp
                    }
                    result.append(submission_dict)
                return result
        except Exception as e:
            logger.error(f"Error getting submissions: {str(e)}")
            raise

    def get_submission_by_id(self, news_id: str) -> Optional[Dict]:
        """
        Get a specific news submission by ID
        
        Args:
            news_id: The ID of the news submission
            
        Returns:
            News submission as dictionary or None if not found
        """
        try:
            with self.get_session() as session:
                record = session.query(SubmissionRecord).filter(
                    SubmissionRecord.id == news_id
                ).first()
                
                if not record:
                    return None
                
                submission = record.to_model()
                # Convert to dict and map field names to match expected API format
                return {
                    "id": submission.id,
                    "title": submission.news_title,
                    "description": submission.news_description,
                    "city": submission.city,
                    "category": submission.category,
                    "reporter_name": submission.publisher_name,
                    "contact_number": submission.publisher_phone,
                    "image_url": submission.image_path,
                    "status": submission.status,
                    "created_at": submission.timestamp
                }
        except Exception as e:
            logger.error(f"Error getting submission by ID: {str(e)}")
            raise
