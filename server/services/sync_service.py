import asyncio
import time
from datetime import datetime
import os
from sqlalchemy.orm import Session
from fastapi import Depends
import traceback

from services.google_sheets import GoogleSheetsService
from services.validation import validate_submission
from services.duplicate_check import DuplicateChecker
from services.image_moderation import ImageModerator
from models import NewsSubmission, ImageModerationResult
from db import crud
from db.database import SessionLocal
from utils.logger import setup_logger
from utils.config_check import check_google_credentials
from utils.helpers import process_drive_image, approve_and_save_image, reject_image
import config

# Set up logger
logger = setup_logger("services.sync")

class SyncService:
    def __init__(self, 
                 interval_seconds: int = 150,  # Default: 5 minutes
                 auto_start: bool = True):
        
        # Check if Google credentials are properly configured
        self.google_sheets_enabled = check_google_credentials()
        
        if self.google_sheets_enabled:
            try:
                self.sheets_service = GoogleSheetsService()
                logger.info("Google Sheets service initialized successfully")
            except Exception as e:
                self.google_sheets_enabled = False
                logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
                logger.error(traceback.format_exc())
        else:
            logger.warning("Google Sheets integration is disabled due to missing configuration")
            
        # Initialize other services
        self.duplicate_checker = DuplicateChecker()
        self.image_moderator = ImageModerator()
        
        # Set up sync parameters
        self.interval = interval_seconds
        self.running = False
        self.last_sync_time = None
        self._task = None
        
        # Track processed row IDs to avoid duplicates
        self.processed_timestamps = set()
        
        if auto_start and self.google_sheets_enabled:
            self.start()
            
    def start(self):
        """Start the synchronization service"""
        if not self.google_sheets_enabled:
            logger.warning("Cannot start sync service: Google Sheets integration is disabled")
            return
            
        if not self.running:
            self.running = True
            self._task = asyncio.create_task(self._sync_loop())
            logger.info(f"Sync service started. Checking for new submissions every {self.interval} seconds.")
        
    def stop(self):
        """Stop the synchronization service"""
        if self.running:
            self.running = False
            if self._task:
                self._task.cancel()
            logger.info("Sync service stopped.")
            
    async def _sync_loop(self):
        """Background task to periodically sync with Google Sheets"""
        while self.running:
            try:
                logger.info("Running Google Sheets synchronization...")
                if self.google_sheets_enabled:
                    await self.sync_submissions()
                    self.last_sync_time = datetime.now()
                    logger.info(f"Sync completed at {self.last_sync_time}. Next sync in {self.interval} seconds.")
                else:
                    logger.warning("Skipping sync: Google Sheets integration is disabled")
            except Exception as e:
                logger.error(f"Error during sync: {str(e)}")
                logger.error(traceback.format_exc())
            
            # Wait for the next interval
            await asyncio.sleep(self.interval)
    
    async def sync_submissions(self):
        """Synchronize new submissions from Google Sheets"""
        # Check if Google Sheets integration is enabled
        if not self.google_sheets_enabled:
            logger.warning("Cannot sync submissions: Google Sheets integration is disabled")
            return
            
        # Get all submissions from Google Sheet
        try:
            submissions = self.sheets_service.get_all_submissions()
        except Exception as e:
            logger.error(f"Failed to get submissions from Google Sheet: {str(e)}")
            logger.error(traceback.format_exc())
            return
        
        if not submissions:
            logger.info("No submissions found in Google Sheet.")
            return
        
        # Get database session
        db = SessionLocal()
        try:
            # Process each submission
            new_count = 0
            for i, sub in enumerate(submissions):
                # Skip if we've already processed this submission (using timestamp as unique identifier)
                if sub.get("timestamp") in self.processed_timestamps:
                    continue
                
                # Process this new submission
                try:
                    logger.info(f"Processing new submission: {sub.get('title')} (timestamp: {sub.get('timestamp')})")
                    
                    # Extract image URL and process it if it's from Google Drive
                    temp_image_path = None
                    permanent_image_path = None
                    original_image_url = sub.get("image_url", "")  # Store the original URL
                    
                    if original_image_url:
                        image_url = original_image_url
                        
                        # Check if it's a Google Drive URL
                        if "drive.google.com" in image_url or "docs.google.com" in image_url:
                            logger.info(f"Processing Google Drive image: {image_url}")
                            success, temp_path, perm_path = process_drive_image(image_url)
                            
                            if success:
                                temp_image_path = temp_path
                                permanent_image_path = perm_path
                                logger.info(f"Google Drive image processed successfully. Temp path: {temp_image_path}")
                            else:
                                logger.warning(f"Failed to process Google Drive image: {perm_path}")
                        else:
                            # For non-Drive URLs, use the existing download function
                            try:
                                from utils.helpers import save_downloaded_image
                                success, result = save_downloaded_image(image_url)
                                if success:
                                    # This is already saved to a permanent location
                                    permanent_image_path = result
                                    logger.info(f"Downloaded image from URL: {permanent_image_path}")
                                else:
                                    logger.warning(f"Failed to download image: {result}")
                            except Exception as img_err:
                                logger.error(f"Error processing image URL: {str(img_err)}")
                    
                    # Create submission object using either the temp or permanent path
                    # For Drive images, we'll use the temporary path initially
                    image_path = temp_image_path or permanent_image_path
                    
                    submission = NewsSubmission(
                        title=sub.get("title", ""),
                        description=sub.get("description", ""),
                        city=sub.get("city", ""),
                        category=sub.get("category", ""),
                        publisher_name=sub.get("publisher_name", ""),
                        publisher_phone=sub.get("publisher_phone", ""),
                        image_path=image_path,
                        original_image_url=original_image_url  # Store the original URL
                    )
                    
                    # Run validation
                    validation_result = validate_submission(submission)
                    
                    # Check for duplicates
                    existing_db = db.query(crud.models.Submission).all()
                    existing_submissions = []
                    for ex_sub in existing_db:
                        existing_submissions.append({
                            "description": ex_sub.description
                        })
                    
                    duplicate_result = self.duplicate_checker.check_duplicate(submission, existing_submissions)
                    
                    # Image moderation
                    moderation_result = None
                    if image_path and os.path.exists(image_path):
                        try:
                            # Try to use the new method that doesn't require sending images to the API
                            moderation_result = self.image_moderator.moderate_image(image_path)
                        except Exception as e:
                            logger.error(f"Error during image moderation: {str(e)}")
                            # Fallback to basic checks if AI moderation fails
                            moderation_result = self.image_moderator.moderate_image_with_fallback(image_path)
                    else:
                        # If no image, mark as inappropriate
                        from models import ImageModerationResult
                        moderation_result = ImageModerationResult(
                            is_appropriate=False,
                            reason="Missing or inaccessible image"
                        )
                    
                    # Handle the final disposition of the image based on moderation results
                    if temp_image_path and permanent_image_path:
                        if moderation_result.is_appropriate and validation_result.is_valid and not duplicate_result.is_duplicate:
                            # If everything is okay, move from temp to permanent location
                            if approve_and_save_image(temp_image_path, permanent_image_path):
                                # Update the image path in the submission to the permanent location
                                submission.image_path = permanent_image_path
                        else:
                            # If there's any issue, reject and delete the temp image
                            reject_image(temp_image_path)
                    
                    # Store in database
                    db_submission = crud.create_submission(
                        db=db,
                        submission=submission,
                        validation=validation_result,
                        duplicate=duplicate_result,
                        moderation=moderation_result
                    )
                    
                    # Mark as processed
                    self.processed_timestamps.add(sub.get("timestamp"))
                    new_count += 1
                    
                    # If submission was rejected, mark it in Google Sheets
                    if not validation_result.is_valid:
                        self.sheets_service.mark_as_invalid(i)
                    elif duplicate_result.is_duplicate:
                        self.sheets_service.mark_as_duplicate(i)
                    elif not moderation_result.is_appropriate:
                        self.sheets_service.mark_as_inappropriate(i)
                        
                    logger.info(f"Processed submission ID {db_submission.id} with status {db_submission.status}")
                    
                except Exception as sub_err:
                    logger.error(f"Error processing submission {i+2}: {str(sub_err)}")
                    logger.error(traceback.format_exc())
                    # Continue with next submission
            
            logger.info(f"Sync complete. Processed {new_count} new submissions.")
            
        finally:
            db.close()
            
    def get_status(self):
        """Get the current status of the sync service"""
        return {
            "running": self.running,
            "google_sheets_enabled": self.google_sheets_enabled,
            "last_sync": self.last_sync_time.isoformat() if self.last_sync_time else None,
            "next_sync": (self.last_sync_time + asyncio.timedelta(seconds=self.interval)).isoformat() 
                         if self.last_sync_time else None,
            "processed_count": len(self.processed_timestamps)
        }
