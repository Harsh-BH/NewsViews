import os
import logging
from typing import Dict, Any, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import settings
from models.news import ProcessedSubmission

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
                spreadsheetId=settings.GOOGLE_SHEET_ID,
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
