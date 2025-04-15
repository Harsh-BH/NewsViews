import os
from pathlib import Path
import config
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("utils.config_check")

def check_google_credentials():
    """Check if Google credentials are properly configured"""
    if not config.GOOGLE_CREDENTIALS_FILE:
        logger.warning("GOOGLE_CREDENTIALS_FILE environment variable is not set")
        return False
    
    # Convert to Path object to handle both absolute and relative paths
    creds_path = Path(config.GOOGLE_CREDENTIALS_FILE)
    
    # If it's a relative path, make it relative to the project root
    if not creds_path.is_absolute():
        creds_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / creds_path
    
    if not creds_path.exists():
        logger.warning(f"Google credentials file not found at: {creds_path}")
        return False
    
    if not config.SPREADSHEET_ID:
        logger.warning("SPREADSHEET_ID environment variable is not set")
        return False
    
    logger.info(f"Google credentials found at: {creds_path}")
    # Update the config value to use the full path
    config.GOOGLE_CREDENTIALS_FILE = str(creds_path)
    return True

def check_groq_api():
    """Check if Groq API is configured"""
    if not config.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY environment variable is not set")
        return False
    return True

def check_database_config():
    """Check if database configuration is valid"""
    if not config.DATABASE_URL:
        logger.warning("DATABASE_URL environment variable is not set")
        return False
    return True

def print_config_status():
    """Print the status of all configuration settings"""
    logger.info("Checking configuration status...")
    
    google_status = check_google_credentials()
    groq_status = check_groq_api()
    db_status = check_database_config()
    
    logger.info(f"Google Sheets integration: {'ENABLED' if google_status else 'DISABLED'}")
    logger.info(f"Groq API integration: {'ENABLED' if groq_status else 'DISABLED'}")
    logger.info(f"Database configuration: {'VALID' if db_status else 'INVALID'}")
    
    return {
        "google_sheets": google_status,
        "groq_api": groq_status,
        "database": db_status
    }
