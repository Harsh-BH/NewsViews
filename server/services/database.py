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

import logging
from typing import Optional, List, Dict, Any
import datetime

from database import get_session
from models.news import ProcessedSubmission

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service for database operations"""
    
    def add_submission(self, submission: ProcessedSubmission) -> bool:
        """
        Add a new submission to the database
        
        Args:
            submission: The submission to add
            
        Returns:
            True if successful, False otherwise
        """
        session = get_session()
        try:
            # Check if submission already exists
            existing = self.get_submission_by_id(submission.id)
            if existing:
                logger.info(f"Submission {submission.id} already exists in database")
                return False
                
            session.add(submission)
            session.commit()
            logger.info(f"Added new submission to database: {submission.id}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add submission: {e}")
            return False
        finally:
            session.close()
    
    def get_submission_by_id(self, submission_id: str) -> Optional[ProcessedSubmission]:
        """
        Get a submission by ID
        
        Args:
            submission_id: The submission ID to look for
            
        Returns:
            The submission if found, None otherwise
        """
        session = get_session()
        try:
            return session.query(ProcessedSubmission).filter(
                ProcessedSubmission.id == submission_id
            ).first()
        except Exception as e:
            logger.error(f"Error querying submission {submission_id}: {e}")
            return None
        finally:
            session.close()
    
    def save_submission(self, submission: ProcessedSubmission) -> bool:
        """
        Save a submission (wrapper around add_submission for compatibility)
        
        Args:
            submission: The submission to save
            
        Returns:
            True if successful, False otherwise
        """
        return self.add_submission(submission)
    
    def get_submissions_by_ids(self, submission_ids: List[str]) -> List[ProcessedSubmission]:
        """
        Get multiple submissions by their IDs
        
        Args:
            submission_ids: List of submission IDs
            
        Returns:
            List of found submissions
        """
        session = get_session()
        try:
            return session.query(ProcessedSubmission).filter(
                ProcessedSubmission.id.in_(submission_ids)
            ).all()
        except Exception as e:
            logger.error(f"Error querying submissions by IDs: {e}")
            return []
        finally:
            session.close()
            
    def get_submissions(self, filters: Dict[str, Any] = None, limit: int = 10, offset: int = 0) -> List[Dict]:
        """
        Get submissions with optional filters and pagination
        
        Args:
            filters: Dictionary of filter conditions
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of submissions formatted as API response dicts
        """
        session = get_session()
        try:
            query = session.query(ProcessedSubmission)
            
            # Apply filters if provided
            if filters and len(filters) > 0:
                for key, value in filters.items():
                    if value is not None and hasattr(ProcessedSubmission, key):
                        query = query.filter(getattr(ProcessedSubmission, key) == value)
            
            # Add ordering and pagination
            query = query.order_by(ProcessedSubmission.timestamp.desc()).limit(limit).offset(offset)
            
            submissions = query.all()
            
            # Convert to API response format
            result = []
            for sub in submissions:
                result.append({
                    "id": sub.id,
                    "title": sub.news_title,
                    "description": sub.news_description,
                    "city": sub.city,
                    "category": sub.category,
                    "reporter_name": sub.publisher_name,
                    "contact_number": sub.publisher_phone,
                    "image_url": sub.image_path,
                    "status": sub.status,
                    "created_at": sub.timestamp
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting submissions: {e}")
            return []
        finally:
            session.close()
    
    def update_submission_status(self, submission_id: str, status: str, duplicate_of: str = None) -> bool:
        """
        Update the status of a submission
        
        Args:
            submission_id: ID of the submission to update
            status: New status value
            duplicate_of: Optional ID of the submission this is a duplicate of
            
        Returns:
            True if successful, False otherwise
        """
        session = get_session()
        try:
            submission = session.query(ProcessedSubmission).filter(
                ProcessedSubmission.id == submission_id
            ).first()
            
            if not submission:
                return False
            
            submission.status = status
            session.commit()
            logger.info(f"Updated status of submission {submission_id} to {status}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating submission status: {e}")
            return False
        finally:
            session.close()
