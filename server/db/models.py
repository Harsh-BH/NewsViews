from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    # Explicitly set the id to Integer type with specific parameters
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    publisher_name = Column(String(100), nullable=False)
    publisher_phone = Column(String(20), nullable=False)
    image_path = Column(String(255))
    original_image_url = Column(String(1000))  # New field for Google Drive URL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status information
    is_valid = Column(Boolean, default=True)
    is_duplicate = Column(Boolean, default=False)
    duplicate_score = Column(Float, nullable=True)
    duplicate_reference_id = Column(String, nullable=True)
    is_appropriate_image = Column(Boolean, default=True)
    status = Column(String(20), default="pending")  # pending, approved, rejected

class ValidationError(Base):
    __tablename__ = "validation_errors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    error_message = Column(Text, nullable=False)
    
    # Define the relationship after both classes exist
    submission = relationship("Submission", back_populates="validation_errors")
    
class ModerationResult(Base):
    __tablename__ = "moderation_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False, unique=True)
    is_appropriate = Column(Boolean, default=True)
    reason = Column(Text, nullable=True)
    
    # Define the relationship after both classes exist
    submission = relationship("Submission", back_populates="moderation_result")

# Now that both dependent classes are defined, add back the relationships to the Submission class
Submission.validation_errors = relationship("ValidationError", back_populates="submission", cascade="all, delete-orphan")
Submission.moderation_result = relationship("ModerationResult", back_populates="submission", uselist=False, cascade="all, delete-orphan")
