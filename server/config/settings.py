import os
import urllib.parse
from typing import Dict, Any, List, Optional, Union
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, model_validator

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # Database settings
    DATABASE_USER: str = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "postgres")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost") 
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "newsviews")
    DATABASE_URL: Optional[str] = None
    
    # Google Sheets settings
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    FORM_RESPONSES_SHEET_ID: str = os.getenv("FORM_RESPONSES_SHEET_ID", "")
    FORM_SYNC_INTERVAL_MINUTES: int = int(os.getenv("FORM_SYNC_INTERVAL_MINUTES", "5"))
    GOOGLE_CREDENTIALS_FILE: str = ""  # Will be set in validator
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "NewsViews API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Upload settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "5"))
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_SHEET_RANGE: str = os.getenv("GOOGLE_SHEET_RANGE", "Form Responses 1")  # Default sheet name to use
    
    
    # Additional settings from .env that might be used
    SPREADSHEET_ID: str = os.getenv("SPREADSHEET_ID", "")
    DUPLICATE_THRESHOLD: float = float(os.getenv("DUPLICATE_THRESHOLD", "0.8"))
    MIN_DESCRIPTION_LENGTH: int = int(os.getenv("MIN_DESCRIPTION_LENGTH", "50"))
    
    @model_validator(mode='after')
    def setup_database_url(self):
        """Set up database URL if not provided directly"""
        try:
            # Check if there's a direct DATABASE_URL in environment
            env_url = os.getenv("DATABASE_URL")
            if env_url:
                # Use the URL directly (already URL-encoded if from .env)
                self.DATABASE_URL = env_url
            else:
                # Construct URL and URL-encode password to handle special characters like @
                password = urllib.parse.quote_plus(self.DATABASE_PASSWORD)
                self.DATABASE_URL = f"postgresql://{self.DATABASE_USER}:{password}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        except Exception as e:
            print(f"Error setting up DATABASE_URL: {e}")
        return self
    
    @model_validator(mode='after')
    def setup_google_credentials(self):
        """Ensure Google credentials file is properly set"""
        try:
            # First check if GOOGLE_CREDENTIALS_FILE is explicitly set
            creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
            
            # If not, use GOOGLE_APPLICATION_CREDENTIALS
            if not creds_file:
                creds_file = self.GOOGLE_APPLICATION_CREDENTIALS
            
            # Make sure it's an absolute path if it's a relative path
            if creds_file and not os.path.isabs(creds_file):
                # Try to find the file in the current directory or project root
                base_paths = [
                    os.getcwd(),  # Current directory
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # Project root
                ]
                
                for base_path in base_paths:
                    full_path = os.path.join(base_path, creds_file)
                    if os.path.isfile(full_path):
                        creds_file = full_path
                        break
            
            # Check if the file exists
            if creds_file and os.path.isfile(creds_file):
                self.GOOGLE_CREDENTIALS_FILE = creds_file
                print(f"Using Google credentials file: {self.GOOGLE_CREDENTIALS_FILE}")
            else:
                print(f"Warning: Google credentials file not found: {creds_file}")
        except Exception as e:
            print(f"Error setting up Google credentials: {e}")
        
        return self
    
    def get_dict(self) -> Dict[str, Any]:
        """Return settings as dictionary (excluding sensitive data)"""
        return {
            "app_name": self.APP_NAME,
            "app_version": self.APP_VERSION,
            "debug": self.DEBUG,
            "database_host": self.DATABASE_HOST,
            "database_name": self.DATABASE_NAME,
            "form_sync_interval": self.FORM_SYNC_INTERVAL_MINUTES,
        }
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }

# Create settings instance
settings = Settings()

# Global constants
APP_NAME = settings.APP_NAME
DEBUG = settings.DEBUG
DATABASE_URL = settings.DATABASE_URL

# Make commonly used settings available at the module level
UPLOAD_DIR = settings.UPLOAD_DIR
FORM_RESPONSES_SHEET_ID = settings.FORM_RESPONSES_SHEET_ID
GOOGLE_APPLICATION_CREDENTIALS = settings.GOOGLE_APPLICATION_CREDENTIALS
OPENAI_API_KEY = settings.OPENAI_API_KEY
# Add this line to expose GOOGLE_SHEET_RANGE at module level
GOOGLE_SHEET_RANGE = settings.GOOGLE_SHEET_RANGE


GOOGLE_CREDENTIALS_FILE = settings.GOOGLE_CREDENTIALS_FILE
SPREADSHEET_ID = settings.SPREADSHEET_ID
DUPLICATE_THRESHOLD = settings.DUPLICATE_THRESHOLD
MIN_DESCRIPTION_LENGTH = settings.MIN_DESCRIPTION_LENGTH
