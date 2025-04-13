import time
import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import threading

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
        self.sheet_range = "Form Responses 1"
        if hasattr(settings, 'GOOGLE_SHEET_RANGE'):
            self.sheet_range = settings.GOOGLE_SHEET_RANGE
            
        self.last_sync_row = 1  # Start from row 1 (header)
        self.last_sync_time = datetime.now() - timedelta(days=1)  # Start with yesterday
        self._running = False
        self._sync_thread = None
        
        # Get column mapping from settings or use defaults
        self.column_mapping = getattr(settings, 'SHEET_COLUMN_MAPPING', {
            'timestamp': 0,
            'title': 1,
            'description': 2,
            'city': 3,
            'category': 4,
            'name': 5,
            'phone': 6
        })
        
        # Load last sync state if available
        self._load_sync_state()
        
    def _load_sync_state(self):
        """Load the last sync state from persistent storage"""
        try:
            # Try to load from a simple state file
            import os
            state_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'form_sync_state.txt')
            if os.path.exists(state_file):
                with open(state_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        self.last_sync_row = int(lines[0].strip())
                        self.last_sync_time = datetime.fromisoformat(lines[1].strip())
                        logger.info(f"Loaded sync state: row {self.last_sync_row}, time {self.last_sync_time}")
        except Exception as e:
            logger.error(f"Failed to load sync state: {e}")
            # Continue with default values
    
    def _save_sync_state(self):
        """Save the current sync state to persistent storage"""
        try:
            # Save to a simple state file
            import os
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            state_file = os.path.join(data_dir, 'form_sync_state.txt')
            with open(state_file, 'w') as f:
                f.write(f"{self.last_sync_row}\n")
                f.write(f"{self.last_sync_time.isoformat()}\n")
        except Exception as e:
            logger.error(f"Failed to save sync state: {e}")
    
    def start_sync_loop(self, interval_seconds: int = 30):
        """
        Start a continuous loop to sync form responses at regular intervals
        
        Args:
            interval_seconds: Seconds to wait between sync operations
        """
        if self._running:
            logger.warning("Sync loop is already running")
            return
            
        self._running = True
        self._sync_thread = threading.Thread(target=self._sync_loop, args=(interval_seconds,))
        self._sync_thread.daemon = True  # Make thread exit when main program exits
        self._sync_thread.start()
        logger.info(f"Started form sync loop with {interval_seconds} second interval")
    
    def _sync_loop(self, interval_seconds: int):
        """
        Internal method for the sync loop thread
        
        Args:
            interval_seconds: Seconds to wait between sync operations
        """
        while self._running:
            try:
                logger.debug("Running scheduled form sync")
                new_count = self.sync()
                
                # Adjust interval based on activity:
                # - If new items found, check again quickly (1/3 of normal interval)
                # - Otherwise, use normal interval
                wait_time = interval_seconds // 3 if new_count > 0 else interval_seconds
                
                logger.debug(f"Next sync in {wait_time} seconds")
                time.sleep(wait_time)
                
            except Exception as e:
                logger.error(f"Error during scheduled sync: {e}")
                # Still wait the regular interval even after error
                time.sleep(interval_seconds)
    
    def stop_sync_loop(self):
        """Stop the continuous sync loop"""
        self._running = False
        if self._sync_thread and self._sync_thread.is_alive():
            self._sync_thread.join(timeout=5.0)
            logger.info("Stopped form sync loop")
    
    def sync(self) -> int:
        """
        Sync Google Forms responses to the database
        
        Returns:
            Number of new items processed
        """
        try:
            logger.debug(f"Fetching form responses from row {self.last_sync_row + 1}")
            
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
                logger.debug("No new form responses found")
                return 0
            
            values = responses.get("values", [])
            processed_count = 0
            
            # Get column headers if this is the first sync
            headers = None
            if self.last_sync_row == 1:
                headers = values[0]
                values = values[1:]  # Skip header row
            
            # Track the maximum row number processed
            max_row_processed = self.last_sync_row
            
            # Process each row
            for row_index, row in enumerate(values):
                try:
                    # Skip empty rows
                    if not row or len(row) < 4:  # Assuming minimum required fields
                        continue
                    
                    current_row = self.last_sync_row + row_index + 1
                    
                    # Skip if we've already processed rows with newer timestamps
                    row_timestamp = self._extract_timestamp(row)
                    if row_timestamp and row_timestamp <= self.last_sync_time:
                        logger.debug(f"Skipping already processed row {current_row} with timestamp {row_timestamp}")
                        max_row_processed = max(max_row_processed, current_row)
                        continue
                    
                    # Create a ProcessedSubmission from the row data
                    submission = self._create_submission_from_row(row, headers)
                    
                    # Check if this submission ID already exists
                    existing = self.db_service.get_submission_by_id(submission.id)
                    if existing:
                        logger.debug(f"Submission {submission.id} already exists in database")
                        max_row_processed = max(max_row_processed, current_row)
                        continue
                    
                    # Save to database
                    self.db_service.add_submission(submission)
                    
                    processed_count += 1
                    max_row_processed = max(max_row_processed, current_row)
                    
                    # Update last sync time if this row has a timestamp
                    if row_timestamp and row_timestamp > self.last_sync_time:
                        self.last_sync_time = row_timestamp
                    
                    logger.info(f"Processed new form response from row {current_row}")
                except Exception as e:
                    logger.error(f"Error processing row {self.last_sync_row + row_index + 1}: {e}")
            
            # Update the last synced row
            if max_row_processed > self.last_sync_row:
                self.last_sync_row = max_row_processed
                # Save sync state for persistence across restarts
                self._save_sync_state()
            
            if processed_count > 0:
                logger.info(f"Form sync completed: {processed_count} new items processed")
            return processed_count
            
        except Exception as e:
            logger.error(f"Form sync failed: {e}")
            return 0
    
    def _extract_timestamp(self, row: List[str]) -> Optional[datetime]:
        """
        Extract timestamp from a row
        
        Args:
            row: Row data from Google Sheet
            
        Returns:
            Datetime object or None if unable to parse
        """
        timestamp_index = self.column_mapping.get('timestamp', 0)
        if timestamp_index < len(row):
            timestamp_str = row[timestamp_index].strip()
            try:
                # Handle common Google Forms timestamp formats
                for fmt in ["%m/%d/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S"]:
                    try:
                        return datetime.strptime(timestamp_str, fmt)
                    except ValueError:
                        continue
                        
                # If all formats fail, try parsing with dateutil as a fallback
                from dateutil import parser
                return parser.parse(timestamp_str)
            except Exception:
                pass
        return None
    
    def _create_submission_from_row(self, row: List[str], headers: List[str] = None) -> ProcessedSubmission:
        """
        Convert a sheet row to a ProcessedSubmission
        
        Args:
            row: Row data from Google Sheet
            headers: Optional column headers
            
        Returns:
            ProcessedSubmission object
        """
        if headers:
            # Map columns based on headers
            header_map = {header.lower().strip(): i for i, header in enumerate(headers)}
            
            # Update column mapping with actual header positions
            for key, default_index in self.column_mapping.items():
                # Look for exact match, then word containing the key
                if key in header_map:
                    self.column_mapping[key] = header_map[key]
                else:
                    # Look for header containing the key
                    for header, idx in header_map.items():
                        if key in header:
                            self.column_mapping[key] = idx
                            break
        
        # Get column indices
        title_index = self.column_mapping.get('title', 1)  
        desc_index = self.column_mapping.get('description', 2)
        city_index = self.column_mapping.get('city', 3)
        category_index = self.column_mapping.get('category', 4)
        name_index = self.column_mapping.get('name', 5)
        phone_index = self.column_mapping.get('phone', 6)
        timestamp_index = self.column_mapping.get('timestamp', 0)
        
        # Get values with safety checks
        def get_safe_value(index):
            return row[index] if index < len(row) else ""
        
        # Generate unique ID - prefer using a unique identifier from the form if available
        # Otherwise generate a UUID
        submission_id = str(uuid.uuid4())
        
        # Parse timestamp if available
        timestamp_str = get_safe_value(timestamp_index)
        timestamp = self._extract_timestamp([timestamp_str]) or datetime.now()
        
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

    def force_sync(self) -> Dict[str, Any]:
        """
        Force immediate synchronization and return results
        
        Returns:
            Dictionary with sync results
        """
        start_time = time.time()
        new_items = self.sync()
        end_time = time.time()
        
        return {
            "success": True,
            "new_items": new_items,
            "duration_seconds": round(end_time - start_time, 2),
            "last_sync_row": self.last_sync_row,
            "last_sync_time": self.last_sync_time.isoformat() if self.last_sync_time else None
        }

# Singleton instance for application-wide use
_instance = None

def get_form_sync_service() -> FormSyncService:
    """
    Get the singleton instance of FormSyncService
    
    Returns:
        FormSyncService instance
    """
    global _instance
    if _instance is None:
        _instance = FormSyncService()
    return _instance

def setup_background_sync(interval_seconds: int = 30):
    """
    Setup background synchronization with Google Sheets
    
    Args:
        interval_seconds: Interval between sync operations in seconds
    """
    service = get_form_sync_service()
    service.start_sync_loop(interval_seconds)
    return service

def main():
    """Main entry point for the form sync service"""
    try:
        sync_service = FormSyncService()
        
        
        # For continuous sync:
        sync_service.start_sync_loop()
    except Exception as e:
        logger.error(f"Error in form sync service: {e}")

if __name__ == "__main__":
    main()
