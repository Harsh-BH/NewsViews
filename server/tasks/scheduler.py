import logging
import time
from threading import Thread, Event
from datetime import datetime, timedelta

from config.settings import settings
from services.sheets_sync import sync_sheets_to_db

logger = logging.getLogger(__name__)

class ScheduledTask:
    """Base class for scheduled tasks"""
    def __init__(self, interval_minutes=5):
        self.interval_minutes = interval_minutes
        self.stop_event = Event()
    
    def run(self):
        """Run the scheduled task"""
        raise NotImplementedError("Subclasses must implement run()")
    
    def start_schedule(self):
        """Start the task on a schedule"""
        next_run = datetime.now()
        
        while not self.stop_event.is_set():
            now = datetime.now()
            
            if now >= next_run:
                try:
                    self.run()
                except Exception as e:
                    logger.error(f"Error running scheduled task: {e}")
                
                # Set next run time
                next_run = datetime.now() + timedelta(minutes=self.interval_minutes)
                logger.info(f"Next run scheduled for {next_run}")
            
            # Sleep for a bit to avoid busy waiting
            time.sleep(10)
    
    def stop(self):
        """Stop the scheduler"""
        self.stop_event.set()


class SheetsSyncTask(ScheduledTask):
    """Task for syncing Google Sheets data to database"""
    def __init__(self):
        super().__init__(interval_minutes=settings.FORM_SYNC_INTERVAL_MINUTES)
        
    def run(self):
        """Sync Google Sheets data with database"""
        logger.info("Running Google Sheets sync task")
        try:
            result = sync_sheets_to_db()
            if "error" in result:
                logger.error(f"Error in sheets sync: {result['error']}")
            else:
                logger.info(f"Sheets sync completed successfully. Added: {result['added']}, "
                           f"Updated: {result['updated']}, Deleted: {result['deleted']}")
        except Exception as e:
            logger.error(f"Exception in sheets sync task: {e}")


# Scheduler to manage all tasks
class Scheduler:
    """Manages scheduled tasks"""
    def __init__(self):
        self.tasks = []
        self.threads = []
    
    def add_task(self, task):
        """Add a task to the scheduler"""
        self.tasks.append(task)
        
    def start(self):
        """Start all tasks"""
        for task in self.tasks:
            thread = Thread(target=task.start_schedule, daemon=True)
            thread.start()
            self.threads.append((thread, task))
            
    def stop(self):
        """Stop all tasks"""
        for _, task in self.threads:
            task.stop()


# Create scheduler instance and add tasks
def init_scheduler():
    """Initialize and start the scheduler"""
    scheduler = Scheduler()
    
    # Add Google Sheets sync task
    sheets_sync_task = SheetsSyncTask()
    scheduler.add_task(sheets_sync_task)
    
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started with all tasks")
    
    return scheduler
