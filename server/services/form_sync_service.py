import time
import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any

from config import settings
from services.google_sheets import GoogleSheetsService
from services.database import DatabaseService
from models.news import ProcessedSubmission

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FormSyncService:
    """Service to sync Google Forms responses with the database"""
    
    def __init__(self):
        """Initialize the form sync service"""
        self.sheets_service = GoogleSheetsService()
        self.db_service = DatabaseService()
        self.spreadsheet_id = settings.FORM_RESPONSES_SHEET_ID
        
        # Fix: Use a default value or get from settings directly
        # Option 1: Use default value
        self.sheet_range = "Form Responses 1"
        # Option 2: Get it from settings if it exists
        if hasattr(settings, 'GOOGLE_SHEET_RANGE'):
            self.sheet_range = settings.GOOGLE_SHEET_RANGE
            
        self.last_sync_row = 1  # Start from row 1 (header)
        
    def start_sync_loop(self, interval_minutes: int = 5):
        """
        Start a continuous loop to sync form responses at regular intervals
        
        Args:
            interval_minutes: Minutes to wait between sync operations
        """
        logger.info(f"Starting form sync loop with {interval_minutes} minute interval")
        interval_seconds = interval_minutes * 60
        
        while True:
            try:
                logger.info("Running scheduled form sync")
                self.sync()
                logger.info(f"Next sync in {interval_minutes} minutes")
            except Exception as e:
                logger.error(f"Error during scheduled sync: {e}")
            
            time.sleep(interval_seconds)
    
    def sync(self) -> int:
        """
        Sync Google Forms responses to the database
        
        Returns:
            Number of new items processed
        """
        try:
            logger.info(f"Fetching form responses from row {self.last_sync_row + 1}")
            
            # Check if spreadsheet ID is set
            if not self.spreadsheet_id:
                logger.error("Form sync failed: No spreadsheet ID configured")
                return 0
                
            # Get sheet data starting from the last synced row + 1
            responses = self.sheets_service.get_sheet_data(
                spreadsheet_id=self.spreadsheet_id,
                range_name=f"{self.sheet_range}!A{self.last_sync_row + 1}:Z"
            )
            
            if responses is None:
                logger.error("Failed to get sheet data - Google Sheets service unavailable")
                return 0
                
            if not responses.get("values", []):
                logger.info("No new form responses found")
                return 0
            
            values = responses.get("values", [])
            processed_count = 0
            
            # Get column headers if this is the first sync
            headers = None
            if self.last_sync_row == 1:
                headers = values[0]
                values = values[1:]  # Skip header row
            
            # Process each row
            for row_index, row in enumerate(values):
                try:
                    # Skip empty rows
                    if not row or len(row) < 4:  # Assuming minimum required fields
                        continue
                    
                    # Create a ProcessedSubmission from the row data
                    submission = self._create_submission_from_row(row, headers)
                    
                    # Save to database - use add_submission instead of save_submission
                    self.db_service.add_submission(submission)
                    
                    processed_count += 1
                    self.last_sync_row = self.last_sync_row + row_index + 1
                    
                    logger.info(f"Processed form response from row {self.last_sync_row}")
                except Exception as e:
                    logger.error(f"Error processing row {self.last_sync_row + row_index + 1}: {e}")
            
            logger.info(f"Form sync completed: {processed_count} new items processed")
            return processed_count
            
        except Exception as e:
            logger.error(f"Form sync failed: {e}")
            raise
    
    def _create_submission_from_row(self, row: List[str], headers: List[str] = None) -> ProcessedSubmission:
        """
        Convert a sheet row to a ProcessedSubmission
        
        Args:
            row: Row data from Google Sheet
            headers: Optional column headers
            
        Returns:
            ProcessedSubmission object
        """
        # Default mapping if no headers provided
        if not headers:
            # Default mapping - adjust based on your actual sheet structure
            title_index = 1  # Assuming title is in column B
            desc_index = 2   # Assuming description is in column C
            city_index = 3   # Assuming city is in column D
            category_index = 4  # Assuming category is in column E
            name_index = 5   # Assuming reporter name is in column F
            phone_index = 6  # Assuming contact number is in column G
            timestamp_index = 0  # Assuming timestamp is in column A
        else:
            # Map columns based on headers
            header_map = {header.lower().strip(): i for i, header in enumerate(headers)}
            
            # Map to indices (with defaults if headers don't match)
            title_index = header_map.get('title', header_map.get('news title', 1))
            desc_index = header_map.get('description', header_map.get('news description', 2))
            city_index = header_map.get('city', 3)
            category_index = header_map.get('category', 4)
            name_index = header_map.get('name', header_map.get('reporter name', 5))
            phone_index = header_map.get('phone', header_map.get('contact number', 6))
            timestamp_index = header_map.get('timestamp', 0)
        
        # Get values with safety checks
        def get_safe_value(index):
            return row[index] if index < len(row) else ""
        
        # Generate unique ID
        submission_id = str(uuid.uuid4())
        
        # Parse timestamp if available
        timestamp_str = get_safe_value(timestamp_index)
        try:
            timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %H:%M:%S")
        except (ValueError, TypeError):
            timestamp = datetime.now()
        
        # Create ProcessedSubmission object
        return ProcessedSubmission(
            id=submission_id,
            news_title=get_safe_value(title_index),
            news_description=get_safe_value(desc_index),
            city=get_safe_value(city_index),
            category=get_safe_value(category_index),
            publisher_name=get_safe_value(name_index),
            publisher_phone=get_safe_value(phone_index),
            image_path=None,  # No image from form
            status="pending",
            timestamp=timestamp
        )

def main():
    """Main entry point for the form sync service"""
    try:
        sync_service = FormSyncService()
        # For a one-time sync:
        # sync_service.sync()
        
        # For continuous sync:
        sync_service.start_sync_loop()
    except Exception as e:
        logger.error(f"Error in form sync service: {e}")

if __name__ == "__main__":
    main()
