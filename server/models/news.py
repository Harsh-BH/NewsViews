from pydantic import BaseModel, Field, validator
from typing import Optional
from config.settings import MIN_DESCRIPTION_LENGTH
import datetime

class NewsSubmission(BaseModel):
    news_title: str
    news_description: str
    city: str
    category: str
    publisher_name: str
    publisher_phone: str
    image_path: Optional[str] = None
    
    @validator('news_description')
    def description_length(cls, v):
        if len(v) < MIN_DESCRIPTION_LENGTH:
            raise ValueError(f'Description must be at least {MIN_DESCRIPTION_LENGTH} characters')
        return v

class ProcessedSubmission(NewsSubmission):
    id: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    status: str = "pending"  # pending, approved, rejected, duplicate
    duplicate_of: Optional[str] = None
    moderation_result: Optional[dict] = None
