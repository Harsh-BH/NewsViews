import os
import logging
from typing import Dict, Any, Optional, List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import settings
from models.news import ProcessedSubmission
from database import get_session

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleSheetsService:
    """Service for interacting with Google Sheets API"""
    
    def __init__(self):
        """Initialize the service with Google credentials"""
        # Initialize service to None in case initialization fails
        self.service = None
        self.credentials = None
        
        try:
            credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS
            logger.info(f"Using Google credentials file: {credentials_path}")
            
            # Check if the credentials file exists
            if not os.path.exists(credentials_path):
                logger.error(f"Google credentials file not found: {credentials_path}")
                return
                
            # Authentication
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path, 
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=self.credentials)
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            logger.error(f"Google Sheets service initialization error: {e}")
            # Don't raise here to allow app to start even if Google Sheets is not available
    
    def _ensure_service(self) -> bool:
        """
        Ensure the Google Sheets service is available
        
        Returns:
            bool: True if service is available, False otherwise
        """
        if self.service is None:
            logger.error("Google Sheets service is not initialized")
            return False
        return True
    
    def append_submission(self, submission: ProcessedSubmission) -> Optional[Dict[str, Any]]:
        """
        Append a submission to the Google Sheet
        
        Args:
            submission: The news submission to append
            
        Returns:
            Response from the Google Sheets API or None if error
        """
        if not self._ensure_service():
            return None
            
        try:
            # Format the data for the sheet
            row_data = [
                submission.id,
                submission.news_title,
                submission.news_description,
                submission.city,
                submission.category,
                submission.publisher_name,
                submission.publisher_phone,
                submission.image_path if submission.image_path else "",
                submission.status,
                submission.timestamp.isoformat() if submission.timestamp else ""
            ]
            
            # Append to sheet
            result = self.service.spreadsheets().values().append(
                spreadsheetId=settings.FORM_RESPONSES_SHEET_ID,
                range=f"{settings.GOOGLE_SHEET_RANGE}!A:J",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={
                    'values': [row_data]
                }
            ).execute()
            
            logger.info(f"Appended submission to sheet: {submission.id}")
            return result
            
        except HttpError as e:
            logger.error(f"Google Sheets API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error appending to Google Sheet: {e}")
            return None
    
    def get_sheet_data(self, spreadsheet_id: str, range_name: str) -> Optional[Dict[str, Any]]:
        """
        Get data from a Google Sheet
        
        Args:
            spreadsheet_id: ID of the Google Sheet
            range_name: Range to retrieve (e.g. 'Sheet1!A1:E10')
            
        Returns:
            Data from the sheet or None if error
        """
        if not self._ensure_service():
            return None
            
        try:
            # Log the spreadsheet and range being accessed
            logger.info(f"Accessing spreadsheet ID: {spreadsheet_id}, range: {range_name}")
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            rows = result.get('values', [])
            logger.info(f"Retrieved {len(rows)} rows from Google Sheets")
            return result
            
        except HttpError as e:
            logger.error(f"Google Sheets API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting data from Google Sheet: {e}")
            return None

    def sync_sheet_to_database(self, spreadsheet_id: str = None, range_name: str = None) -> Dict[str, int]:
        """
        Sync data from Google Sheet to database, avoiding duplicate entries
        
        Args:
            spreadsheet_id: ID of the Google Sheet (defaults to settings.FORM_RESPONSES_SHEET_ID)
            range_name: Range to retrieve (defaults to settings.GOOGLE_SHEET_RANGE)
            
        Returns:
            Dict with counts of added, skipped, and error entries
        """
        if not self._ensure_service():
            return {"added": 0, "skipped": 0, "errors": 0}
            
        # Use default values from settings if not provided
        spreadsheet_id = spreadsheet_id or settings.FORM_RESPONSES_SHEET_ID
        range_name = range_name or f"{settings.GOOGLE_SHEET_RANGE}!A:J"
        
        try:
            # Get data from sheet
            result = self.get_sheet_data(spreadsheet_id, range_name)
            if not result:
                logger.error("Failed to retrieve sheet data")
                return {"added": 0, "skipped": 0, "errors": 0}
                
            rows = result.get('values', [])
            if not rows:
                logger.info("No data found in sheet")
                return {"added": 0, "skipped": 0, "errors": 0}
                
            # Skip header row if present (assuming first row is header)
            if rows[0][0].lower() == "id" or not rows[0][0].strip().isalnum():
                data_rows = rows[1:]
            else:
                data_rows = rows
                
            stats = {"added": 0, "skipped": 0, "errors": 0}
            
            # Get database session
            db_session = get_session()
            
            # Process each row
            for row in data_rows:
                try:
                    # Skip rows with insufficient data
                    if len(row) < 9:
                        stats["errors"] += 1
                        logger.warning(f"Skipping row with insufficient data: {row}")
                        continue
                        
                    submission_id = row[0].strip()
                    
                    # Check if submission already exists in database
                    existing_submission = db_session.query(ProcessedSubmission).filter(
                        ProcessedSubmission.id == submission_id
                    ).first()
                    
                    if existing_submission:
                        logger.info(f"Submission {submission_id} already exists, skipping")
                        stats["skipped"] += 1
                        continue
                        
                    # Create new submission object
                    new_submission = ProcessedSubmission(
                        id=submission_id,
                        news_title=row[1],
                        news_description=row[2],
                        city=row[3],
                        category=row[4],
                        publisher_name=row[5],
                        publisher_phone=row[6],
                        image_path=row[7] if len(row) > 7 and row[7].strip() else None,
                        status=row[8] if len(row) > 8 and row[8].strip() else "pending",
                        timestamp=row[9] if len(row) > 9 and row[9].strip() else None
                    )
                    
                    # Add to database
                    db_session.add(new_submission)
                    db_session.commit()
                    stats["added"] += 1
                    logger.info(f"Added new submission from sheet: {submission_id}")
                    
                except Exception as e:
                    db_session.rollback()
                    stats["errors"] += 1
                    logger.error(f"Error processing row: {e}")
                    
            logger.info(f"Sheet sync complete. Added: {stats['added']}, "
                       f"Skipped: {stats['skipped']}, Errors: {stats['errors']}")
            return stats
            
        except Exception as e:
            logger.error(f"Error syncing sheet to database: {e}")
            return {"added": 0, "skipped": 0, "errors": 0}
        finally:
            if 'db_session' in locals():
                db_session.close()
