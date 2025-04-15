#!/usr/bin/env python3
"""
Script to reset the database by dropping and recreating all tables.
USE WITH CAUTION: This will delete all existing data!
"""
import os
import sys
import argparse

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import engine, Base
from db import models
import config
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("db.reset")

def reset_database(confirm=False):
    """Drop all tables and recreate them"""
    if not confirm:
        confirm = input(f"This will delete ALL DATA in {config.DATABASE_URL}! Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("Operation cancelled.")
            return False
    
    logger.warning(f"Dropping all tables in database")
    # Drop all tables
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping tables: {str(e)}")
        return False
    
    # Recreate all tables
    try:
        logger.info("Creating new tables")
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reset the database by dropping and recreating all tables.")
    parser.add_argument("--force", action="store_true", help="Force reset without confirmation")
    args = parser.parse_args()
    
    if reset_database(confirm=args.force):
        print("Database reset successfully!")
    else:
        print("Database reset failed. Check the logs for details.")
        sys.exit(1)
