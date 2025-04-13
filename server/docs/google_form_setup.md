# Setting Up Google Form Integration

This document explains how to set up Google Forms to collect news submissions and have them automatically processed by our application.

## 1. Create a Google Form

1. Go to [Google Forms](https://forms.google.com) and create a new form
2. Add the following questions to match your data model:
   - News Title (Short answer)
   - News Description (Paragraph)
   - City (Short answer)
   - Category (Dropdown or Multiple choice)
   - Your Name (Short answer)
   - Contact Number (Short answer)
   - Any other fields you need

## 2. Configure Form Settings

1. Click on the Settings ⚙️ icon
2. Under "Responses" tab, ensure "Collect email addresses" is OFF (unless needed)
3. Under "General" tab, consider enabling "Limit to 1 response" if appropriate

## 3. Link Form to Google Sheets

1. Go to "Responses" tab at the top of your form
2. Click the Google Sheets icon 📊
3. Select "Create a new spreadsheet" or link to an existing one
4. Note the name of the created spreadsheet

## 4. Get the Spreadsheet ID

1. Open the responses spreadsheet
2. The URL will look like: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
3. Copy the `SPREADSHEET_ID` portion

## 5. Set Up Google Cloud Project and Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API and Google Drive API for your project
4. Navigate to "IAM & Admin" > "Service Accounts"
5. Click "Create Service Account"
6. Provide a service account name and description
7. Grant necessary roles (at least "Editor" role for Google Sheets)
8. Click "Create and Continue" then "Done"
9. Click on the newly created service account from the list
10. Go to the "Keys" tab and click "Add Key" > "Create new key"
11. Choose JSON format and click "Create"
12. The credentials file will be downloaded to your computer
13. The service account email address has the format: `service-account-name@project-id.iam.gserviceaccount.com`

## 6. Update Your Configuration

1. Move the downloaded JSON credentials file to a secure location in your project
2. Set the path to this file in your `.env` or `config.py`:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-credentials.json
   FORM_RESPONSES_SHEET_ID=your_spreadsheet_id
   ```
3. You can open the credentials file with a text editor to verify the service account email address (look for the "client_email" field)

## 7. Share the Spreadsheet with Service Account

1. Get the email address of your service account from the credentials file (the "client_email" field)
2. In Google Sheets, click "Share" in the top right
3. Enter the service account email and give it "Editor" access
4. Click "Share"

## 8. Test the Integration

1. Submit a test response through your Google Form
2. Wait for the sync interval (default: 5 minutes) or restart your application
3. Check your application's database to verify the submission was processed

## Column Mapping

Ensure your Form questions match these expected column names in the spreadsheet:

| Form Question   | Expected Column Name |
|-----------------|---------------------|
| News Title      | News Title          |
| News Description| News Description    |
| City            | City                |
| Category        | Category            |
| Your Name       | Your Name           |
| Contact Number  | Contact Number      |

If your form uses different column names, you'll need to update the mapping in `form_sync_service.py`.
