import os
import sys

# Add parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.oauth2 import service_account
import gspread
from config import settings

def test_google_sheets_access():
    """Test access to Google Sheets with current settings"""
    
    print(f"Testing Google Sheets access with:")
    print(f"- Credentials file: {settings.GOOGLE_CREDENTIALS_FILE}")
    print(f"- Spreadsheet ID: {settings.SPREADSHEET_ID}")
    
    try:
        # Check if credentials file exists
        if not os.path.isfile(settings.GOOGLE_CREDENTIALS_FILE):
            print(f"ERROR: Credentials file not found at: {settings.GOOGLE_CREDENTIALS_FILE}")
            if os.path.isabs(settings.GOOGLE_CREDENTIALS_FILE):
                print("The path is absolute. Make sure the file exists at this location.")
            else:
                print("The path is relative. Current working directory:", os.getcwd())
                print("Checking in current directory...")
                if os.path.isfile(os.path.join(os.getcwd(), settings.GOOGLE_APPLICATION_CREDENTIALS)):
                    full_path = os.path.join(os.getcwd(), settings.GOOGLE_APPLICATION_CREDENTIALS)
                    print(f"Found file at: {full_path}")
                    print("Update your settings to use this path.")
            return
            
        # Try to authenticate
        print("Attempting to authenticate...")
        credentials = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        client = gspread.authorize(credentials)
        print("Authentication successful!")
        
        # Try to open the spreadsheet
        print(f"Attempting to open spreadsheet with ID: {settings.SPREADSHEET_ID}")
        sheet = client.open_by_key(settings.SPREADSHEET_ID)
        print(f"Successfully opened spreadsheet: {sheet.title}")
        
        # List worksheets
        worksheets = sheet.worksheets()
        print(f"Available worksheets: {[ws.title for ws in worksheets]}")
        
        print("\nGoogle Sheets access test PASSED!")
        
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify the credentials file exists and is valid")
        print("2. Make sure the service account has been given access to the spreadsheet")
        print("   - Share your Google Sheet with the client_email from your credentials file")
        print("3. Verify the spreadsheet ID is correct")
        print("   - It's the long string in the URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
        
if __name__ == "__main__":
    test_google_sheets_access()
