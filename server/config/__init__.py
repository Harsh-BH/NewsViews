# Initialize config module
from .settings import (
    settings,
    APP_NAME, 
    DEBUG,
    DATABASE_URL,
    UPLOAD_DIR,
    FORM_RESPONSES_SHEET_ID,
    GOOGLE_APPLICATION_CREDENTIALS,
    OPENAI_API_KEY,
 
    GOOGLE_CREDENTIALS_FILE,
    SPREADSHEET_ID,
    DUPLICATE_THRESHOLD,
    MIN_DESCRIPTION_LENGTH
)

# Export all the variables and settings object
__all__ = [
    'settings',
    'APP_NAME',
    'DEBUG',
    'DATABASE_URL',
    'UPLOAD_DIR',
    'FORM_RESPONSES_SHEET_ID',
    'GOOGLE_APPLICATION_CREDENTIALS',
    'OPENAI_API_KEY',

    'GOOGLE_CREDENTIALS_FILE',
    'SPREADSHEET_ID',
    'DUPLICATE_THRESHOLD',
    'MIN_DESCRIPTION_LENGTH'
]
