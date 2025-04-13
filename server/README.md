# NewsViews Server

This is the server component of the NewsViews application, which allows collecting news submissions through Google Forms.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/NewsViews.git
   cd NewsViews/server
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure the environment variables by creating a `.env` file:
   ```
   # Copy the example file
   cp .env.example .env
   
   # Edit the .env file with your settings
   nano .env
   ```

4. The `.env` file should contain:
   ```
   # Database settings
   DATABASE_USER=postgres
   DATABASE_PASSWORD=yourpassword
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=newsviews
   
   # Google Sheets settings
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
   FORM_RESPONSES_SHEET_ID=your_spreadsheet_id
   ```

5. Follow the instructions in [Google Form Setup](docs/google_form_setup.md) to configure your Google Form integration.

## Running the Application

### Main Application Server

To run the main application server:

```
python app.py
```

The server will start on http://localhost:5000 by default.

### Form Sync Service

The Form Sync Service automatically syncs submissions from Google Forms to your database.

#### Running as a standalone process

```
python services/form_sync_service.py
```

By default, it will sync every 5 minutes.

#### Running as a scheduled task

Alternatively, you can set up a cron job or scheduled task to run the sync process:

1. For Linux/macOS (cron job):
   ```
   # Edit your crontab
   crontab -e
   
   # Add this line to run every 5 minutes
   */5 * * * * cd /path/to/NewsViews/server && /path/to/python services/form_sync_service.py
   ```

2. For Windows (Task Scheduler):
   - Open Task Scheduler
   - Create Basic Task
   - Set trigger to "Daily" and recur every 5 minutes
   - Action: Start a program
   - Program/script: `path\to\python.exe`
   - Arguments: `services\form_sync_service.py`
   - Start in: `path\to\NewsViews\server`

## Development

### Project Structure

```
server/
  ├── app.py              # Main application entry point
  ├── config.py           # Application configuration
  ├── requirements.txt    # Python dependencies
  ├── models/             # Database models
  ├── services/           # Service components
  │   └── form_sync_service.py  # Google Forms sync service
  ├── routes/             # API routes
  └── docs/               # Documentation
      └── google_form_setup.md  # Google Form setup guide
```

### Adding New Features

1. Create or modify models in the `models/` directory
2. Add new routes in the `routes/` directory
3. Implement business logic in the `services/` directory

## Troubleshooting

### Form Sync Issues

If the form sync service is not working:

1. Check that your Google credentials file is correct and has the right permissions
2. Verify that the service account has access to the Google Sheet
3. Check the column mappings in `form_sync_service.py` match your Google Form questions
4. Look for error messages in the application logs

### API Issues

If the API is not responding:

1. Check that the server is running
2. Verify database connection settings
3. Check the application logs for errors

## License

[Your License Here]
