# Google Form & Sheet Setup Guide

This guide explains how to set up your Google Form and Google Sheet for use with the NewsViews application.

## Google Form Setup

### Required Form Fields

Create a Google Form with the following fields in this order:

1. **News Title**
   - Field Type: Short answer
   - Required: Yes

2. **News Description**
   - Field Type: Paragraph
   - Required: Yes
   - Validation: Minimum character count = 50

3. **City**
   - Field Type: Short answer or Dropdown
   - Required: Yes

4. **Topic/Category**
   - Field Type: Dropdown
   - Required: Yes
   - Suggested options: Accident, Festival, Community Event, Sports, Weather, Business, Education

5. **Publisher's First Name**
   - Field Type: Short answer
   - Required: Yes

6. **Publisher's Phone Number**
   - Field Type: Short answer
   - Required: Yes
   - Suggested validation: Phone number

7. **Image Upload**
   - Field Type: File upload
   - Required: Yes
   - File types: Accept only image files (JPG, JPEG, PNG)
   - Maximum number of files: 1

### Form Settings

1. Go to the Settings gear icon
2. Under "Responses" tab, ensure "Collect email addresses" is OFF to keep submissions anonymous
3. Under "Presentation" tab, you may want to show a progress bar
4. Under "Defaults" tab, you can customize the confirmation message

### Response Destination

1. Click on the "Responses" tab in your form
2. Click the Google Sheets icon (Create Spreadsheet)
3. Select "Create a new spreadsheet" or "Select existing spreadsheet"
4. Note the URL of the spreadsheet - you'll need the ID from this URL

## Google Sheets Configuration

After creating your form, a linked Google Sheet will be created with these columns:

1. Timestamp
2. News Title
3. News Description
4. City
5. Topic/Category
6. Publisher's First Name
7. Publisher's Phone Number
8. Image Upload

The system will automatically add these columns for administrative use:

- Column I: Duplicate status
- Column J: Content moderation status
- Column K: Validation status

### Getting Your Spreadsheet ID

The Spreadsheet ID is the part in the URL between `/d/` and `/edit`:
```
https://docs.google.com/spreadsheets/d/[THIS-IS-YOUR-SPREADSHEET-ID]/edit
```

## Google Service Account Setup

To allow the NewsViews application to access your Google Sheet:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the Google Sheets API for your project
4. Create service account credentials:
   - Navigate to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill out the service account details
   - Grant the service account "Editor" access to the project
   - Create a key (JSON format) for the service account
   - Download the JSON key file

5. Share your Google Sheet with the service account email address (found in the JSON file under "client_email")

## Configuration in NewsViews

1. Place the downloaded JSON credentials file in your server's credentials directory
2. Update your `.env` file with these settings:
   ```
   GOOGLE_CREDENTIALS_FILE=path/to/your-credentials.json
   SPREADSHEET_ID=your-spreadsheet-id-from-url
   ```

3. Restart the server to apply the changes

## Testing the Integration

After setting up:

1. Submit a test entry through your Google Form
2. Wait for the sync interval (default: 5 minutes) or trigger a manual sync
3. Check the NewsViews API at `/submissions/db` to verify the entry was processed
