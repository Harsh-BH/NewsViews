import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Sheets configuration
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# Groq API configuration (replacing OpenAI)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# App settings
DUPLICATE_THRESHOLD = float(os.getenv("DUPLICATE_THRESHOLD", "0.8"))
MIN_DESCRIPTION_LENGTH = int(os.getenv("MIN_DESCRIPTION_LENGTH", "50"))

# Supported image formats
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/newsviews"
)

# Image moderation settings
USE_AI_MODERATION = os.getenv("USE_AI_MODERATION", "true").lower() == "true"
