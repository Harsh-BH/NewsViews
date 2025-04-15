from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from services.google_sheets import GoogleSheetsService
from services.validation import validate_submission
from services.duplicate_check import DuplicateChecker
from services.image_moderation import ImageModerator
from models import NewsSubmission, ValidationResult, DuplicateCheckResult, ImageModerationResult
from utils.helpers import save_uploaded_image
from db.database import get_db
from db import crud, models
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("routers.submissions")

router = APIRouter(
    prefix="/submissions",
    tags=["submissions"],
    responses={404: {"description": "Not found"}}
)

# Dependency injection
def get_sheets_service():
    return GoogleSheetsService()

def get_duplicate_checker():
    return DuplicateChecker()

def get_image_moderator():
    return ImageModerator()

@router.get("/", response_model=List[dict])
async def get_submissions(
    sheets_service: GoogleSheetsService = Depends(get_sheets_service)
):
    """Get all news submissions from Google Sheets"""
    try:
        logger.info("Fetching submissions from Google Sheets")
        return sheets_service.get_all_submissions()
    except Exception as e:
        logger.error(f"Failed to retrieve submissions from Google Sheets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve submissions: {str(e)}")

@router.get("/db", response_model=List[dict])
async def get_submissions_from_db(
    skip: int = Query(0, description="Skip records"),
    limit: int = Query(100, description="Limit records"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Get submissions from the database"""
    try:
        logger.info(f"Fetching submissions from database (skip={skip}, limit={limit}, status={status})")
        
        if status:
            submissions = crud.get_submissions_by_status(db, status, skip, limit)
        else:
            submissions = crud.get_all_submissions(db, skip, limit)
            
        logger.info(f"Found {len(submissions)} submissions")
        
        # Convert SQLAlchemy models to dictionaries
        result = []
        for submission in submissions:
            result.append({
                "id": submission.id,
                "title": submission.title,
                "description": submission.description,
                "city": submission.city,
                "category": submission.category,
                "publisher_name": submission.publisher_name,
                "publisher_phone": submission.publisher_phone,
                "image_path": submission.image_path,
                "original_image_url": submission.original_image_url,  # Include original URL
                "created_at": submission.created_at,
                "status": submission.status,
                "is_valid": submission.is_valid,
                "is_duplicate": submission.is_duplicate,
                "is_appropriate_image": submission.is_appropriate_image
            })
            
        return result
        
    except Exception as e:
        logger.error(f"Failed to retrieve submissions from database: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve submissions: {str(e)}")

@router.get("/db/{submission_id}", response_model=dict)
async def get_submission_by_id(
    submission_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific submission by ID"""
    submission = crud.get_submission(db, submission_id)
    if not submission:
        logger.warning(f"Submission with ID {submission_id} not found")
        raise HTTPException(status_code=404, detail="Submission not found")
    
    logger.info(f"Retrieved submission {submission_id}")
    
    # Convert to dictionary
    result = {
        "id": submission.id,
        "title": submission.title,
        "description": submission.description,
        "city": submission.city,
        "category": submission.category,
        "publisher_name": submission.publisher_name,
        "publisher_phone": submission.publisher_phone,
        "image_path": submission.image_path,
        "original_image_url": submission.original_image_url,  # Include original URL
        "created_at": submission.created_at,
        "status": submission.status,
        "is_valid": submission.is_valid,
        "is_duplicate": submission.is_duplicate,
        "is_appropriate_image": submission.is_appropriate_image
    }
    
    return result

@router.post("/validate")
async def validate_news_submission(
    title: str = Form(...),
    description: str = Form(...),
    city: str = Form(...),
    category: str = Form(...),
    publisher_name: str = Form(...),
    publisher_phone: str = Form(...),
    image: UploadFile = File(...),
    sheets_service: GoogleSheetsService = Depends(get_sheets_service),
    duplicate_checker: DuplicateChecker = Depends(get_duplicate_checker),
    image_moderator: ImageModerator = Depends(get_image_moderator),
    db: Session = Depends(get_db)
):
    """Validate a news submission including duplicate check and image moderation"""
    logger.info(f"Processing new submission: {title}")
    
    # Step 1: Save the uploaded image
    success, result = save_uploaded_image(image)
    if not success:
        logger.error(f"Failed to save image: {result}")
        raise HTTPException(status_code=400, detail=result)
    
    image_path = result
    logger.info(f"Image saved to: {image_path}")
    
    # Step 2: Create a submission object
    submission = NewsSubmission(
        title=title,
        description=description,
        city=city,
        category=category,
        publisher_name=publisher_name,
        publisher_phone=publisher_phone,
        image_path=image_path
    )
    
    # Step 3: Validate basic fields
    logger.info("Validating submission fields")
    validation_result = validate_submission(submission)
    if not validation_result.is_valid:
        logger.warning(f"Validation failed: {validation_result.errors}")
        # Clean up the uploaded file since validation failed
        if os.path.exists(image_path):
            os.remove(image_path)
            logger.info(f"Removed invalid submission image: {image_path}")
        return {"status": "error", "validation": validation_result.dict()}
    
    # Step 4: Check for duplicate content
    logger.info("Checking for duplicate content")
    existing_submissions = sheets_service.get_all_submissions()
    duplicate_result = duplicate_checker.check_duplicate(submission, existing_submissions)
    
    # Step 5: Check image appropriateness
    logger.info("Checking image appropriateness")
    moderation_result = image_moderator.moderate_image(image_path)
    
    # Step 6: Store in database
    logger.info("Storing submission results in database")
    db_submission = crud.create_submission(
        db=db,
        submission=submission,
        validation=validation_result,
        duplicate=duplicate_result,
        moderation=moderation_result
    )
    
    # Compile results
    result = {
        "validation": validation_result.dict(),
        "duplicate_check": duplicate_result.dict(),
        "image_moderation": moderation_result.dict(),
        "submission_id": db_submission.id
    }
    
    # Overall status
    if (not validation_result.is_valid or 
        duplicate_result.is_duplicate or 
        not moderation_result.is_appropriate):
        result["status"] = "rejected"
        logger.warning(f"Submission rejected: ID={db_submission.id}")
        # Clean up the uploaded file since submission was rejected
        if os.path.exists(image_path):
            os.remove(image_path)
            logger.info(f"Removed rejected submission image: {image_path}")
    else:
        result["status"] = "approved"
        logger.info(f"Submission approved: ID={db_submission.id}")
    
    return result
