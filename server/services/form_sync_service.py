import datetime
import uuid
from typing import List, Dict, Any
import os
import time
import logging
from datetime import datetime
import googleapiclient.discovery
from google.oauth2 import service_account

# Import from the consolidated config
from config import settings

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class FormSyncService:
    def __init__(self):
        self.spreadsheet_id = settings.FORM_RESPONSES_SHEET_ID
        self.credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS
        self.last_sync_row = 1  # Start from row 2 (header is row 1)
        self.column_mapping = {
            'News Title': 'title',
            'News Description': 'description',
            'City': 'city',
            'Category': 'category',
            'Your Name': 'reporter_name',
            'Contact Number': 'contact_number'
        }
        
        if not self.spreadsheet_id:
            raise ValueError("FORM_RESPONSES_SHEET_ID setting is not set")
        
        if not self.credentials_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS setting is not set")

    def get_sheets_service(self):
        """Create and return a Google Sheets service object"""
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path, scopes=scopes)
        service = googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)
        return service

    def get_form_responses(self):
        """Fetch new responses from the Google Sheet"""
        try:
            service = self.get_sheets_service()
            sheets = service.spreadsheets()
            
            # First, get the header row to map columns
            result = sheets.values().get(
                spreadsheetId=self.spreadsheet_id,
                range='Form Responses 1!A1:Z1'
            ).execute()
            headers = result.get('values', [[]])[0]
            
            # Next, get all rows after the last synced row
            result = sheets.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f'Form Responses 1!A{self.last_sync_row + 1}:Z'
            ).execute()
            rows = result.get('values', [])
            
            if not rows:
                logger.info("No new responses found")
                return []
                
            # Process the rows
            news_items = []
            for i, row in enumerate(rows):
                if len(row) < len(headers):
                    row.extend([''] * (len(headers) - len(row)))
                
                news_item = {}
                for j, header in enumerate(headers):
                    if header in self.column_mapping:
                        news_item[self.column_mapping[header]] = row[j]
                
                news_item['source'] = 'google_form'
                news_item['submitted_at'] = datetime.now().isoformat()
                news_items.append(news_item)
                
            # Update the last synced row
            self.last_sync_row += len(rows)
            logger.info(f"Fetched {len(rows)} new responses")
            return news_items
            
        except Exception as e:
            logger.error(f"Error fetching form responses: {e}")
            return []

    def save_to_database(self, news_items):
        """Save the news items to the database"""
        try:
            # This is where you would save the data to your database
            # Example using SQLAlchemy:
            # for item in news_items:
            #     news = News(
            #         title=item.get('title', ''),
            #         description=item.get('description', ''),
            #         city=item.get('city', ''),
            #         category=item.get('category', ''),
            #         reporter_name=item.get('reporter_name', ''),
            #         contact_number=item.get('contact_number', ''),
            #         source=item.get('source', ''),
            #         submitted_at=item.get('submitted_at')
            #     )
            #     db_session.add(news)
            # db_session.commit()
            
            # For now, just log the items
            for item in news_items:
                logger.info(f"Would save to database: {item}")
                
            logger.info(f"Successfully processed {len(news_items)} news items")
            return True
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            return False

    def sync(self):
        """Sync data from Google Forms to the database"""
        logger.info("Starting form sync process")
        news_items = self.get_form_responses()
        if news_items:
            self.save_to_database(news_items)
        return len(news_items)

    def start_sync_loop(self, interval_minutes=None):
        """Start a continuous sync loop with the specified interval"""
        # Use the setting from config if not specified
        if interval_minutes is None:
            interval_minutes = settings.FORM_SYNC_INTERVAL_MINUTES
            
        logger.info(f"Starting sync loop with {interval_minutes} minute interval")
        while True:
            self.sync()
            logger.info(f"Sleeping for {interval_minutes} minutes")
            time.sleep(interval_minutes * 60)

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
