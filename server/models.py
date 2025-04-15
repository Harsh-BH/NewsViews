from pydantic import BaseModel, Field, validator
import config

class NewsSubmission(BaseModel):
    title: str
    description: str
    city: str
    category: str
    publisher_name: str
    publisher_phone: str
    image_path: str = None
    original_image_url: str = None  # New field for original URL

    @validator("description")
    def validate_description_length(cls, v):
        if len(v) < config.MIN_DESCRIPTION_LENGTH:
            raise ValueError(f"Description must be at least {config.MIN_DESCRIPTION_LENGTH} characters long")
        return v

class ValidationResult(BaseModel):
    is_valid: bool
    errors: list[str] = []

class ImageModerationResult(BaseModel):
    is_appropriate: bool
    reason: str = None

class DuplicateCheckResult(BaseModel):
    is_duplicate: bool
    similarity_score: float = None
    duplicate_entry_id: str = None
