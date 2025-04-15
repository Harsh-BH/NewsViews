import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import config

class GoogleSheetsService:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            config.GOOGLE_CREDENTIALS_FILE, 
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.spreadsheet_id = config.SPREADSHEET_ID

    def get_all_submissions(self):
        """Fetch all submissions from Google Sheet"""
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self.spreadsheet_id,
            range='Form Responses 1!A2:H'  # Assuming headers are in row 1
        ).execute()
        values = result.get('values', [])
        
        submissions = []
        for row in values:
            # Make sure we have enough columns
            if len(row) >= 7:
                submission = {
                    "timestamp": row[0] if len(row) > 0 else "",
                    "title": row[1] if len(row) > 1 else "",
                    "description": row[2] if len(row) > 2 else "",
                    "city": row[3] if len(row) > 3 else "",
                    "category": row[4] if len(row) > 4 else "",
                    "publisher_name": row[5] if len(row) > 5 else "",
                    "publisher_phone": row[6] if len(row) > 6 else "",
                    "image_url": row[7] if len(row) > 7 else ""
                }
                submissions.append(submission)
        
        return submissions

    def mark_as_duplicate(self, row_index):
        """Mark a submission as duplicate in the sheet"""
        sheet = self.service.spreadsheets()
        sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f'Form Responses 1!I{row_index + 2}',  # Column I, accounting for header
            valueInputOption='RAW',
            body={'values': [['DUPLICATE']]}
        ).execute()

    def mark_as_inappropriate(self, row_index):
        """Mark a submission as having inappropriate content"""
        sheet = self.service.spreadsheets()
        sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f'Form Responses 1!J{row_index + 2}',  # Column J
            valueInputOption='RAW',
            body={'values': [['INAPPROPRIATE CONTENT']]}
        ).execute()

    def mark_as_invalid(self, row_index):
        """Mark a submission as having invalid fields"""
        sheet = self.service.spreadsheets()
        sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f'Form Responses 1!K{row_index + 2}',  # Column K
            valueInputOption='RAW',
            body={'values': [['INVALID SUBMISSION']]}
        ).execute()
