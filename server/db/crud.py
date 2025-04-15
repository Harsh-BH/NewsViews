from sqlalchemy.orm import Session
from db import models
from models import NewsSubmission, ValidationResult, DuplicateCheckResult, ImageModerationResult
from typing import List
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("db.crud")

def create_submission(
    db: Session,
    submission: NewsSubmission,
    validation: ValidationResult,
    duplicate: DuplicateCheckResult,
    moderation: ImageModerationResult
) -> models.Submission:
    """Create a new submission record with validation, duplicate check, and moderation results"""
    
    # Determine overall status
    status = "approved"
    if not validation.is_valid or duplicate.is_duplicate or not moderation.is_appropriate:
        status = "rejected"
    
    # Create the submission
    db_submission = models.Submission(
        title=submission.title,
        description=submission.description,
        city=submission.city,
        category=submission.category,
        publisher_name=submission.publisher_name,
        publisher_phone=submission.publisher_phone,
        image_path=submission.image_path,
        original_image_url=submission.original_image_url,  # Store the original URL
        is_valid=validation.is_valid,
        is_duplicate=duplicate.is_duplicate,
        duplicate_score=duplicate.similarity_score,
        duplicate_reference_id=duplicate.duplicate_entry_id,
        is_appropriate_image=moderation.is_appropriate,
        status=status
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    logger.info(f"Created submission ID {db_submission.id} with status {status}")
    
    # Add validation errors if any
    if validation.errors:
        for error in validation.errors:
            db_error = models.ValidationError(
                submission_id=db_submission.id,
                error_message=error
            )
            db.add(db_error)
        
        db.commit()
        logger.info(f"Added {len(validation.errors)} validation errors for submission {db_submission.id}")
    
    # Add moderation result
    if not moderation.is_appropriate and moderation.reason:
        db_moderation = models.ModerationResult(
            submission_id=db_submission.id,
            is_appropriate=moderation.is_appropriate,
            reason=moderation.reason
        )
        db.add(db_moderation)
        db.commit()
        logger.info(f"Added moderation result for submission {db_submission.id}: {moderation.reason}")
    
    return db_submission

def get_all_submissions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Submission]:
    """Get all submissions with pagination"""
    return db.query(models.Submission).order_by(models.Submission.created_at.desc()).offset(skip).limit(limit).all()

def get_submission(db: Session, submission_id: int) -> models.Submission:
    """Get a specific submission by ID"""
    return db.query(models.Submission).filter(models.Submission.id == submission_id).first()

def get_submissions_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[models.Submission]:
    """Get submissions by status (approved, rejected, pending)"""
    return db.query(models.Submission).filter(models.Submission.status == status).order_by(models.Submission.created_at.desc()).offset(skip).limit(limit).all()
