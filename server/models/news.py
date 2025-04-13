from pydantic import BaseModel, Field
from typing import Optional
import datetime
import uuid

class NewsSubmission(BaseModel):
    """Model for news submission from users"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    city: str
    category: str
    reporter_name: str
    contact_number: str
    image_url: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

class ProcessedSubmission(BaseModel):
    """Model for processed news submission with status"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    # Field aliases to match both API and database field names
    title: Optional[str] = None
    news_title: str  # Main field used in database
    description: Optional[str] = None
    news_description: str  # Main field used in database
    city: str
    category: str
    reporter_name: Optional[str] = None
    publisher_name: str  # Main field used in database
    contact_number: Optional[str] = None
    publisher_phone: str  # Main field used in database
    image_url: Optional[str] = None
    image_path: Optional[str] = None  # Main field used in database
    status: str = "pending"
    created_at: Optional[datetime.datetime] = None
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)  # Main field used in database
    
    # Add compatibility methods and field mappings
    def dict(self, *args, **kwargs):
        """Custom dict method to support both field names"""
        base_dict = super().dict(*args, **kwargs)
        # Ensure all fields have values even when provided with different names
        if not base_dict.get("news_title") and base_dict.get("title"):
            base_dict["news_title"] = base_dict["title"]
        if not base_dict.get("news_description") and base_dict.get("description"):
            base_dict["news_description"] = base_dict["description"]
        if not base_dict.get("publisher_name") and base_dict.get("reporter_name"):
            base_dict["publisher_name"] = base_dict["reporter_name"]
        if not base_dict.get("publisher_phone") and base_dict.get("contact_number"):
            base_dict["publisher_phone"] = base_dict["contact_number"]
        if not base_dict.get("image_path") and base_dict.get("image_url"):
            base_dict["image_path"] = base_dict["image_url"]
        if not base_dict.get("timestamp") and base_dict.get("created_at"):
            base_dict["timestamp"] = base_dict["created_at"]
        return base_dict
