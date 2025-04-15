"""
Utility for managing temporary file storage
"""
import os
import tempfile
import time
import uuid
import shutil
from datetime import datetime, timedelta
from typing import List, Optional
import threading
from utils.logger import setup_logger

# Set up logger
logger = setup_logger("utils.temp_storage")

class TempStorageManager:
    """Manage temporary storage of files"""
    
    def __init__(self, base_dir=None, expiry_minutes=60):
        """
        Initialize the temporary storage manager
        
        Args:
            base_dir: Base directory for temporary files (default: system temp dir + 'newsviews_temp')
            expiry_minutes: Time in minutes until temporary files expire (default: 60)
        """
        if base_dir:
            self.temp_dir = base_dir
        else:
            self.temp_dir = os.path.join(tempfile.gettempdir(), 'newsviews_temp')
            
        # Create the directory if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)
        
        self.expiry_minutes = expiry_minutes
        self._cleanup_thread = None
        self._shutdown = False
        
    def get_temp_path(self, prefix="img_", suffix=".jpg") -> str:
        """
        Get a path for a new temporary file
        
        Args:
            prefix: Prefix for the filename
            suffix: Suffix for the filename (usually file extension)
            
        Returns:
            Path to the temporary file
        """
        unique_id = uuid.uuid4().hex
        return os.path.join(self.temp_dir, f"{prefix}{unique_id}{suffix}")
        
    def save_temp_file(self, file_data, prefix="img_", suffix=".jpg") -> str:
        """
        Save data to a temporary file
        
        Args:
            file_data: Binary data to save
            prefix: Prefix for the filename
            suffix: Suffix for the filename
            
        Returns:
            Path to the saved temporary file
        """
        temp_path = self.get_temp_path(prefix, suffix)
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(file_data)
            logger.info(f"Saved temporary file: {temp_path}")
            return temp_path
        except Exception as e:
            logger.error(f"Error saving temporary file: {str(e)}")
            return None
            
    def move_to_permanent(self, temp_path: str, permanent_path: str) -> bool:
        """
        Move a temporary file to a permanent location
        
        Args:
            temp_path: Path to the temporary file
            permanent_path: Path to the permanent location
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(permanent_path), exist_ok=True)
            
            # Move the file
            shutil.move(temp_path, permanent_path)
            logger.info(f"Moved temporary file to permanent location: {temp_path} -> {permanent_path}")
            return True
        except Exception as e:
            logger.error(f"Error moving temporary file to permanent location: {str(e)}")
            return False
            
    def get_expired_files(self) -> List[str]:
        """
        Get a list of expired temporary files
        
        Returns:
            List of paths to expired files
        """
        expired_files = []
        now = datetime.now()
        
        for file_name in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file_name)
            
            # Skip directories
            if not os.path.isfile(file_path):
                continue
                
            # Check if the file has expired
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - modified_time > timedelta(minutes=self.expiry_minutes):
                expired_files.append(file_path)
                
        return expired_files
        
    def cleanup_expired_files(self) -> int:
        """
        Delete expired temporary files
        
        Returns:
            Number of files deleted
        """
        expired_files = self.get_expired_files()
        
        for file_path in expired_files:
            try:
                os.remove(file_path)
                logger.info(f"Deleted expired temporary file: {file_path}")
            except Exception as e:
                logger.error(f"Error deleting expired temporary file: {file_path} - {str(e)}")
                
        return len(expired_files)
        
    def start_cleanup_thread(self, interval_minutes=15):
        """
        Start a background thread to periodically clean up expired files
        
        Args:
            interval_minutes: Time in minutes between cleanup runs
        """
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            logger.warning("Cleanup thread is already running")
            return
            
        self._shutdown = False
        
        def cleanup_task():
            logger.info("Starting temporary file cleanup thread")
            while not self._shutdown:
                deleted_count = self.cleanup_expired_files()
                logger.info(f"Temporary file cleanup completed. Deleted {deleted_count} files")
                
                # Sleep for the specified interval
                for _ in range(interval_minutes * 60):
                    if self._shutdown:
                        break
                    time.sleep(1)
            
            logger.info("Temporary file cleanup thread stopped")
            
        self._cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
        self._cleanup_thread.start()
        logger.info(f"Started temporary file cleanup thread. Interval: {interval_minutes} minutes")
        
    def stop_cleanup_thread(self):
        """Stop the background cleanup thread"""
        if not self._cleanup_thread or not self._cleanup_thread.is_alive():
            logger.warning("No cleanup thread is running")
            return
            
        self._shutdown = True
        self._cleanup_thread.join(timeout=5)
        logger.info("Stopped temporary file cleanup thread")
        
# Create a global instance of the temporary storage manager
temp_storage = TempStorageManager()
