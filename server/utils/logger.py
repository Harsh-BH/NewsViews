import logging
import sys
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logger
def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create a formatter that includes timestamp, level, and message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Terminal handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    # File handler - create a new log file each day
    today = datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(f"logs/newsviews_{today}.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
