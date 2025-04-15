"""
Migration script to add original_image_url column to submissions table
"""
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import Column, String, text
from db.database import engine
from utils.logger import setup_logger

logger = setup_logger("db.migration")

def add_original_image_url_column():
    """Add original_image_url column to submissions table"""
    try:
        # Check if column already exists
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='submissions' AND column_name='original_image_url';
            """))
            column_exists = result.fetchone() is not None
            
            if column_exists:
                logger.info("Column 'original_image_url' already exists in submissions table")
                return True
                
            # Add the column
            conn.execute(text("""
                ALTER TABLE submissions
                ADD COLUMN original_image_url VARCHAR(1000);
            """))
            conn.commit()
            
            logger.info("Successfully added 'original_image_url' column to submissions table")
            return True
            
    except Exception as e:
        logger.error(f"Error adding column: {str(e)}")
        return False

if __name__ == "__main__":
    if add_original_image_url_column():
        print("Migration completed successfully.")
    else:
        print("Migration failed. Check the logs for details.")
        sys.exit(1)
