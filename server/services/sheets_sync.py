import logging
from typing import List, Dict, Any, Set, Optional
import gspread
from google.oauth2 import service_account
from sqlalchemy.orm import Session

from config.settings import settings
from database.models import Submission
from database.database import get_db

logger = logging.getLogger(__name__)

class SheetsSyncService:
    """Service for syncing data between Google Sheets and the database, including tracking deletions"""
    
    def __init__(self):
        """Initialize the service with Google credentials"""
        try:
            self.creds = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_CREDENTIALS_FILE,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.client = gspread.authorize(self.creds)
            self.sheet_id = settings.SPREADSHEET_ID or settings.FORM_RESPONSES_SHEET_ID
            self.sheet_range = settings.GOOGLE_SHEET_RANGE
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets client: {e}")
            raise

    def get_sheet_data(self) -> List[Dict[str, Any]]:
        """Fetch data from Google Sheet and return as list of dictionaries"""
        try:
            sheet = self.client.open_by_key(self.sheet_id).worksheet(self.sheet_range)
            records = sheet.get_all_records()
            return records
        except Exception as e:
            logger.error(f"Failed to get sheet data: {e}")
            return []
    
    def get_sheet_submission_ids(self) -> Set[str]:
        """Get all submission IDs currently in the Google Sheet"""
        sheet_data = self.get_sheet_data()
        # Use the appropriate ID field from your sheet - adjust as needed
        submission_ids = {str(row.get('ID', row.get('id', row.get('Timestamp', '')))) 
                         for row in sheet_data if row}
        return submission_ids
    
    def get_database_submission_ids(self, db: Session) -> Set[str]:
        """Get all submission IDs currently in the database"""
        submissions = db.query(Submission.id).all()
        return {str(sub.id) for sub in submissions}

    def delete_missing_submissions(self, db: Session) -> int:
        """Delete submissions from database that are no longer in the Google Sheet
        
        Returns:
            int: Number of deleted submissions
        """
        try:
            # Get IDs from both sources
            sheet_ids = self.get_sheet_submission_ids()
            db_ids = self.get_database_submission_ids(db)
            
            # Find IDs that exist in database but not in sheet (deleted from sheet)
            deleted_ids = db_ids - sheet_ids
            
            if not deleted_ids:
                logger.info("No submissions to delete, sheet and database are in sync")
                return 0
                
            # Delete submissions that no longer exist in the sheet
            delete_count = db.query(Submission).filter(
                Submission.id.in_(deleted_ids)
            ).delete(synchronize_session=False)
            
            db.commit()
            
            logger.info(f"Deleted {delete_count} submissions that were removed from the Google Sheet")
            return delete_count
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error during deletion sync: {e}")
            return 0

    def sync_sheet_to_db(self, db: Session) -> Dict[str, int]:
        """
        Sync Google Sheet data to database including handling deletions
        
        Returns:
            Dict with counts of added, updated, and deleted submissions
        """
        result = {"added": 0, "updated": 0, "deleted": 0}
        
        try:
            # First check for and handle any deleted submissions
            deleted_count = self.delete_missing_submissions(db)
            result["deleted"] = deleted_count
            
            # Then proceed with normal sync logic for additions and updates
            # ... existing sync logic goes here ...
            
            return result
        except Exception as e:
            logger.error(f"Error in sheets sync: {e}")
            return result

# Create a singleton instance
sheets_sync_service = SheetsSyncService()

def sync_sheets_to_db():
    """Function to be called from scheduler or API endpoint"""
    db = next(get_db())
    try:
        result = sheets_sync_service.sync_sheet_to_db(db)
        return result
    except Exception as e:
        logger.error(f"Error in sheets sync: {e}")
        return {"error": str(e)}
    finally:
        db.close()
