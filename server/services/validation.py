from models.news import NewsSubmission
from config import settings
import re

class ValidationService:
    @staticmethod
    def validate_submission(submission: NewsSubmission) -> tuple[bool, str]:
        """Validates a news submission and returns (is_valid, error_message)"""
        
        # Check if all required fields are filled
        for field in settings.FORM_FIELDS:
            if not getattr(submission, field, None):
                return False, f"Field '{field}' is required"
        
        # Validate description length
        if len(submission.news_description) < settings.MIN_DESCRIPTION_LENGTH:
            return False, f"News description must be at least {settings.MIN_DESCRIPTION_LENGTH} characters"
            
        # Validate phone number (simple validation)
        if not re.match(r'^\+?[\d\s()-]{8,15}$', submission.publisher_phone):
            return False, "Invalid phone number format"
            
        return True, ""
