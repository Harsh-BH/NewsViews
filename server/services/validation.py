from models import NewsSubmission, ValidationResult
import config
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("services.validation")

def validate_submission(submission: NewsSubmission) -> ValidationResult:
    """Validate a news submission"""
    errors = []
    
    # Check for empty fields
    if not submission.title.strip():
        errors.append("News title cannot be empty")
        
    if not submission.description.strip():
        errors.append("News description cannot be empty")
    elif len(submission.description) < config.MIN_DESCRIPTION_LENGTH:
        errors.append(f"News description must be at least {config.MIN_DESCRIPTION_LENGTH} characters long")
        
    if not submission.city.strip():
        errors.append("City cannot be empty")
        
    if not submission.category.strip():
        errors.append("Category cannot be empty")
        
    if not submission.publisher_name.strip():
        errors.append("Publisher's name cannot be empty")
        
    if not submission.publisher_phone.strip():
        errors.append("Publisher's phone number cannot be empty")
    
    # Check if image was uploaded
    if submission.image_path is None:
        errors.append("Image must be uploaded")
    
    is_valid = len(errors) == 0
    
    if is_valid:
        logger.info(f"Submission validation passed: {submission.title}")
    else:
        logger.warning(f"Submission validation failed: {submission.title} - Errors: {errors}")
    
    return ValidationResult(
        is_valid=is_valid,
        errors=errors
    )
