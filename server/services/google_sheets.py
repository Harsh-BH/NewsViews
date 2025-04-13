import os
import logging
import gspread
from google.oauth2 import service_account
from config import settings
import uuid
import datetime
from models.news import NewsSubmission, ProcessedSubmission

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    """Service for interacting with Google Sheets"""
    
    def __init__(self):
        """Initialize Google Sheets service"""
        try:
            # Verify if credentials file exists
            if not os.path.exists(settings.GOOGLE_CREDENTIALS_FILE):
                raise FileNotFoundError(f"Google credentials file not found: {settings.GOOGLE_CREDENTIALS_FILE}")
                
            logger.info(f"Initializing Google Sheets service with credentials: {settings.GOOGLE_CREDENTIALS_FILE}")
            logger.info(f"Spreadsheet ID: {settings.SPREADSHEET_ID}")
            
            # Create credentials
            credentials = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_CREDENTIALS_FILE,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            # Authorize and create client
            self.client = gspread.authorize(credentials)
            
            # Try to open the spreadsheet - first try SPREADSHEET_ID, fallback to FORM_RESPONSES_SHEET_ID
            try:
                sheet_id = settings.SPREADSHEET_ID
                self.sheet = self.client.open_by_key(sheet_id)
                logger.info(f"Successfully opened spreadsheet: {self.sheet.title}")
            except gspread.exceptions.SpreadsheetNotFound:
                # Try the alternative sheet ID if available
                if settings.FORM_RESPONSES_SHEET_ID and settings.FORM_RESPONSES_SHEET_ID != settings.SPREADSHEET_ID:
                    logger.warning(f"Spreadsheet not found with ID: {settings.SPREADSHEET_ID}. Trying FORM_RESPONSES_SHEET_ID...")
                    sheet_id = settings.FORM_RESPONSES_SHEET_ID
                    self.sheet = self.client.open_by_key(sheet_id)
                    logger.info(f"Successfully opened spreadsheet with FORM_RESPONSES_SHEET_ID: {self.sheet.title}")
                else:
                    raise
                    
            # Get all available worksheets
            self.worksheets = self.sheet.worksheets()
            logger.info(f"Available worksheets: {[ws.title for ws in self.worksheets]}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {str(e)}", exc_info=True)
            print("\nIMPORTANT: The service account needs access to the Google Sheet!")
            print("Please share your Google Sheet with the service account email from your credentials file.")
            raise
    
    def _initialize_sheets(self):
        try:
            self.submissions_sheet = self.sheet.worksheet("Submissions")
        except gspread.exceptions.WorksheetNotFound:
            self.submissions_sheet = self.sheet.add_worksheet(
                title="Submissions", 
                rows=1000, 
                cols=10
            )
            # Add headers
            self.submissions_sheet.append_row([
                "ID", "Timestamp", "Title", "Description", "City", 
                "Category", "Publisher Name", "Publisher Phone", 
                "Image Path", "Status"
            ])
    
    def get_all_submissions(self):
        records = self.submissions_sheet.get_all_records()
        submissions = []
        
        for record in records:
            # Skip header row
            if record.get("ID") == "ID":
                continue
                
            submission = ProcessedSubmission(
                id=record.get("ID", ""),
                timestamp=datetime.datetime.fromisoformat(record.get("Timestamp", datetime.datetime.now().isoformat())),
                news_title=record.get("Title", ""),
                news_description=record.get("Description", ""),
                city=record.get("City", ""),
                category=record.get("Category", ""),
                publisher_name=record.get("Publisher Name", ""),
                publisher_phone=record.get("Publisher Phone", ""),
                image_path=record.get("Image Path", ""),
                status=record.get("Status", "pending")
            )
            submissions.append(submission)
            
        return submissions
    
    def add_submission(self, submission: ProcessedSubmission):
        row = [
            submission.id,
            submission.timestamp.isoformat(),
            submission.news_title,
            submission.news_description,
            submission.city,
            submission.category,
            submission.publisher_name,
            submission.publisher_phone,
            submission.image_path or "",
            submission.status
        ]
        self.submissions_sheet.append_row(row)
    
    def update_submission_status(self, submission_id: str, status: str, duplicate_of: str = None):
        records = self.submissions_sheet.get_all_records()
        
        for i, record in enumerate(records, start=2):  # Start from 2 to account for header row
            if record.get("ID") == submission_id:
                self.submissions_sheet.update_cell(i, 10, status)  # Status is in column J (10)
                if duplicate_of:
                    # Add a note about the duplicate
                    self.submissions_sheet.update_cell(
                        i, 4, f"{record.get('Description')} [DUPLICATE of {duplicate_of}]"
                    )
                return True
                
        return False
