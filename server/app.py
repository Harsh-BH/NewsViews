from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid
import datetime
import shutil
import time
import logging
import threading
from typing import List, Dict, Optional, Any, Set
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import gspread
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import from the consolidated config
from config import settings, UPLOAD_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ====================================
# Database Setup
# ====================================
# Use the proper import path for declarative_base
Base = declarative_base()

class ProcessedSubmission(Base):
    """Database model for news submissions"""
    __tablename__ = "submissions"
    
    id = Column(String(36), primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    news_title = Column(String(200), nullable=False)
    news_description = Column(Text, nullable=False)
    city = Column(String(100))
    category = Column(String(50))
    publisher_name = Column(String(100))
    publisher_phone = Column(String(20))
    image_path = Column(String(500))
    status = Column(String(20), default="pending")
    
    def to_dict(self):
        """Convert to dictionary for API response"""
        return {
            "id": self.id,
            "title": self.news_title,
            "description": self.news_description,
            "city": self.city,
            "category": self.category,
            "reporter_name": self.publisher_name,
            "contact_number": self.publisher_phone,
            "image_url": self.image_path,
            "status": self.status,
            "created_at": self.timestamp
        }

# Create engine and session factory
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(engine)

def get_session():
    """Get database session"""
    session = SessionLocal()
    try:
        return session
    finally:
        session.close()

# ====================================
# Google Sheets Service
# ====================================
class GoogleSheetsService:
    """Service for interacting with Google Sheets API"""
    
    def __init__(self):
        """Initialize the service with Google credentials"""
        self.service = None
        
        try:
            credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS
            logger.info(f"Using Google credentials file: {credentials_path}")
            
            # Check if credentials file exists
            if not os.path.exists(credentials_path):
                logger.error(f"Google credentials file not found: {credentials_path}")
                return
                
            # Authenticate
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, 
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            logger.error(f"Google Sheets service initialization error: {e}")
    
    def get_sheet_data(self, spreadsheet_id=None, range_name=None):
        """Get data from a Google Sheet"""
        if not self.service:
            logger.error("Google Sheets service is not initialized")
            return None
            
        spreadsheet_id = spreadsheet_id or settings.FORM_RESPONSES_SHEET_ID
        range_name = range_name or f"{settings.GOOGLE_SHEET_RANGE}!A:Z"
        
        try:
            logger.info(f"Getting data from sheet: {spreadsheet_id}, range: {range_name}")
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            rows = result.get('values', [])
            logger.info(f"Retrieved {len(rows)} rows from Google Sheets")
            return rows
            
        except Exception as e:
            logger.error(f"Error getting sheet data: {e}")
            return None
    
    def append_submission(self, submission):
        """Append a submission to the Google Sheet"""
        if not self.service:
            logger.error("Google Sheets service is not initialized")
            return None
            
        try:
            # Format the data for the sheet
            row_data = [
                submission.id,
                submission.news_title,
                submission.news_description,
                submission.city,
                submission.category,
                submission.publisher_name,
                submission.publisher_phone,
                submission.image_path if submission.image_path else "",
                submission.status,
                submission.timestamp.isoformat() if submission.timestamp else ""
            ]
            
            # Append to sheet
            self.service.spreadsheets().values().append(
                spreadsheetId=settings.FORM_RESPONSES_SHEET_ID,
                range=f"{settings.GOOGLE_SHEET_RANGE}!A:J",
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={
                    'values': [row_data]
                }
            ).execute()
            
            logger.info(f"Appended submission to sheet: {submission.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error appending to Google Sheet: {e}")
            return False

# ====================================
# Database Operations
# ====================================
class DatabaseService:
    """Service for database operations"""
    
    def add_submission(self, submission_data):
        """Add a submission to the database"""
        session = SessionLocal()
        try:
            # Check if submission with this ID already exists
            existing = session.query(ProcessedSubmission).filter(
                ProcessedSubmission.id == submission_data.get("id")
            ).first()
            
            if existing:
                logger.debug(f"Submission {submission_data.get('id')} already exists")
                return False
            
            # Create new submission
            submission = ProcessedSubmission(
                id=submission_data.get("id"),
                news_title=submission_data.get("news_title", submission_data.get("title", "")),
                news_description=submission_data.get("news_description", submission_data.get("description", "")),
                city=submission_data.get("city", ""),
                category=submission_data.get("category", ""),
                publisher_name=submission_data.get("publisher_name", submission_data.get("reporter_name", "")),
                publisher_phone=submission_data.get("publisher_phone", submission_data.get("contact_number", "")),
                image_path=submission_data.get("image_path", submission_data.get("image_url", "")),
                status=submission_data.get("status", "pending"),
                timestamp=submission_data.get("timestamp", datetime.datetime.now())
            )
            
            session.add(submission)
            session.commit()
            logger.info(f"Added submission to database: {submission.id}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding submission: {e}")
            return False
        finally:
            session.close()
    
    def get_submissions(self, filters=None, limit=10, offset=0):
        """Get submissions with optional filters"""
        session = SessionLocal()
        try:
            query = session.query(ProcessedSubmission)
            
            # Apply filters
            if filters:
                for key, value in filters.items():
                    if value is not None and hasattr(ProcessedSubmission, key):
                        query = query.filter(getattr(ProcessedSubmission, key) == value)
            
            # Order and paginate
            submissions = query.order_by(ProcessedSubmission.timestamp.desc()).limit(limit).offset(offset).all()
            
            # Convert to dictionaries
            return [s.to_dict() for s in submissions]
            
        except Exception as e:
            logger.error(f"Error getting submissions: {e}")
            return []
        finally:
            session.close()
    
    def get_submission_by_id(self, submission_id):
        """Get a specific submission by ID"""
        session = SessionLocal()
        try:
            submission = session.query(ProcessedSubmission).filter(
                ProcessedSubmission.id == submission_id
            ).first()
            
            if submission:
                return submission.to_dict()
            return None
            
        except Exception as e:
            logger.error(f"Error getting submission by ID: {e}")
            return None
        finally:
            session.close()
    
    def count_submissions(self):
        """Count total submissions in database"""
        session = SessionLocal()
        try:
            return session.query(ProcessedSubmission).count()
        except Exception as e:
            logger.error(f"Error counting submissions: {e}")
            return 0
        finally:
            session.close()

# ====================================
# Sync Service
# ====================================
class SheetSyncService:
    """Service to sync Google Sheets with database"""
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
        self.db_service = DatabaseService()
        self._running = False
        self._sync_thread = None
        self.last_sync_time = datetime.datetime.now() - datetime.timedelta(days=1)
        
        # Load mappings between sheet columns and database fields
        self.column_mapping = {
            'id': 0,
            'news_title': 1,
            'news_description': 2,
            'city': 3,
            'category': 4,
            'publisher_name': 5,
            'publisher_phone': 6,
            'image_path': 7,
            'status': 8,
            'timestamp': 9
        }
    
    def sync_sheets_to_db(self):
        """Synchronize data from Google Sheets to database"""
        try:
            # Check if database is empty
            db_count = self.db_service.count_submissions()
            is_db_empty = db_count == 0
            
            logger.info(f"Database has {db_count} submissions. Empty: {is_db_empty}")
            
            # Get data from sheet
            rows = self.sheets_service.get_sheet_data()
            if not rows:
                logger.warning("No data retrieved from Google Sheets")
                return {"added": 0, "skipped": 0}
                
            # Skip header row if it exists
            if rows[0][0].lower() == "id" or not rows[0][0].strip().isalnum():
                data_rows = rows[1:]
            else:
                data_rows = rows
                
            # Process rows
            added = 0
            skipped = 0
            
            for row in data_rows:
                try:
                    # Skip rows with insufficient data
                    if len(row) < 4:
                        logger.debug(f"Skipping row with insufficient data: {row}")
                        continue
                    
                    # Extract submission ID
                    if len(row) > 0 and row[0].strip():
                        submission_id = row[0].strip()
                    else:
                        submission_id = str(uuid.uuid4())
                    
                    # Extract timestamp if available
                    timestamp = None
                    if len(row) > 9 and row[9].strip():
                        try:
                            timestamp_str = row[9].strip()
                            # Try common formats
                            for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M:%S"]:
                                try:
                                    timestamp = datetime.datetime.strptime(timestamp_str, fmt)
                                    break
                                except ValueError:
                                    continue
                        except Exception:
                            timestamp = datetime.datetime.now()
                    else:
                        timestamp = datetime.datetime.now()
                    
                    # Skip if we already processed this entry (based on ID or timestamp)
                    if not is_db_empty:
                        existing = self.db_service.get_submission_by_id(submission_id)
                        if existing:
                            logger.debug(f"Skipping existing submission: {submission_id}")
                            skipped += 1
                            continue
                        
                        # Also skip if older than last sync time (unless DB was empty)
                        if timestamp and timestamp < self.last_sync_time:
                            logger.debug(f"Skipping submission with old timestamp: {timestamp}")
                            skipped += 1
                            continue
                    
                    # Create submission data
                    submission_data = {
                        "id": submission_id,
                        "news_title": row[1] if len(row) > 1 else "",
                        "news_description": row[2] if len(row) > 2 else "",
                        "city": row[3] if len(row) > 3 else "",
                        "category": row[4] if len(row) > 4 else "",
                        "publisher_name": row[5] if len(row) > 5 else "",
                        "publisher_phone": row[6] if len(row) > 6 else "",
                        "image_path": row[7] if len(row) > 7 and row[7].strip() else None,
                        "status": row[8] if len(row) > 8 and row[8].strip() else "pending",
                        "timestamp": timestamp
                    }
                    
                    # Add to database
                    success = self.db_service.add_submission(submission_data)
                    if success:
                        added += 1
                        # Update last sync time if needed
                        if timestamp and timestamp > self.last_sync_time:
                            self.last_sync_time = timestamp
                    else:
                        skipped += 1
                        
                except Exception as e:
                    logger.error(f"Error processing row: {e}")
                    skipped += 1
            
            logger.info(f"Sheet sync complete. Added: {added}, Skipped: {skipped}")
            return {"added": added, "skipped": skipped}
            
        except Exception as e:
            logger.error(f"Error in sheets sync: {e}")
            return {"added": 0, "skipped": 0, "error": str(e)}
    
    def start_sync_loop(self, interval_seconds=30):
        """Start continuous background sync"""
        if self._running:
            return False
            
        self._running = True
        self._sync_thread = threading.Thread(target=self._sync_loop, args=(interval_seconds,))
        self._sync_thread.daemon = True
        self._sync_thread.start()
        logger.info(f"Started sync loop with {interval_seconds}s interval")
        return True
    
    def _sync_loop(self, interval_seconds):
        """Background sync loop implementation"""
        while self._running:
            try:
                # Run sync
                result = self.sync_sheets_to_db()
                items_added = result.get("added", 0)
                
                # Adjust wait time based on activity
                wait_time = interval_seconds // 3 if items_added > 0 else interval_seconds
                time.sleep(wait_time)
                
            except Exception as e:
                logger.error(f"Error in sync loop: {e}")
                time.sleep(interval_seconds)
    
    def stop_sync_loop(self):
        """Stop the background sync loop"""
        self._running = False
        if self._sync_thread and self._sync_thread.is_alive():
            self._sync_thread.join(timeout=5)
        logger.info("Stopped sync loop")

    def get_sheet_submission_ids(self) -> Set[str]:
        """Get all submission IDs currently in the Google Sheet"""
        sheet_data = self.sheets_service.get_sheet_data()
        # Use the appropriate ID field from your sheet - adjust as needed
        submission_ids = {str(row[0]) for row in sheet_data if row}
        return submission_ids
    
    def get_database_submission_ids(self) -> Set[str]:
        """Get all submission IDs currently in the database"""
        session = SessionLocal()
        try:
            submissions = session.query(ProcessedSubmission.id).all()
            return {str(sub.id) for sub in submissions}
        finally:
            session.close()

    def delete_missing_submissions(self) -> int:
        """Delete submissions from database that are no longer in the Google Sheet
        
        Returns:
            int: Number of deleted submissions
        """
        session = SessionLocal()
        try:
            # Get IDs from both sources
            sheet_ids = self.get_sheet_submission_ids()
            db_ids = self.get_database_submission_ids()
            
            # Find IDs that exist in database but not in sheet (deleted from sheet)
            deleted_ids = db_ids - sheet_ids
            
            if not deleted_ids:
                logger.info("No submissions to delete, sheet and database are in sync")
                return 0
                
            # Delete submissions that no longer exist in the sheet
            delete_count = session.query(ProcessedSubmission).filter(
                ProcessedSubmission.id.in_(deleted_ids)
            ).delete(synchronize_session=False)
            
            session.commit()
            
            logger.info(f"Deleted {delete_count} submissions that were removed from the Google Sheet")
            return delete_count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error during deletion sync: {e}")
            return 0
        finally:
            session.close()

    def sync_sheet_to_db(self) -> Dict[str, int]:
        """
        Sync Google Sheet data to database including handling deletions
        
        Returns:
            Dict with counts of added, updated, and deleted submissions
        """
        result = {"added": 0, "updated": 0, "deleted": 0}
        
        try:
            # First check for and handle any deleted submissions
            deleted_count = self.delete_missing_submissions()
            result["deleted"] = deleted_count
            
            # Then proceed with normal sync logic for additions and updates
            # Add your existing sync logic here
            # For now, we'll just log that this part would happen
            logger.info("Would process additions and updates here")
            
            return result
        except Exception as e:
            logger.error(f"Error in sheets sync: {e}")
            return result

# ====================================
# FastAPI Setup
# ====================================
app = FastAPI(
    title=settings.APP_NAME,
    description="API for NewsViews application",
    version=settings.APP_VERSION
)

# Initialize services
db_service = DatabaseService()
sheets_service = GoogleSheetsService()
sync_service = SheetSyncService()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Request/Response models
class NewsResponse(BaseModel):
    id: str
    title: str
    description: str
    city: str
    category: str
    reporter_name: str
    contact_number: str
    image_url: Optional[str] = None
    status: str
    created_at: datetime.datetime

# ====================================
# Application Lifecycle Events
# ====================================
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        logger.info("Starting NewsViews application...")
        
        # Initial sync with Google Sheets - this will populate database if empty
        results = sync_service.sync_sheets_to_db()
        logger.info(f"Initial sync results: {results}")
        
        # Start background sync process
        sync_service.start_sync_loop(interval_seconds=30)
        logger.info("Background sync started")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    try:
        # Stop background sync
        sync_service.stop_sync_loop()
        logger.info("Background sync stopped")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# ====================================
# API Endpoints
# ====================================
@app.get("/")
async def root():
    """API root endpoint"""
    return {"message": "Welcome to NewsViews API", "status": "operational"}

@app.post("/news", response_model=NewsResponse)
async def submit_news(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    description: str = Form(...),
    city: str = Form(...),
    category: str = Form(...),
    reporter_name: str = Form(...),
    contact_number: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    """Submit a news item"""
    try:
        # Generate unique ID
        news_id = str(uuid.uuid4())
        
        # Handle image upload if provided
        image_url = None
        if image:
            file_extension = os.path.splitext(image.filename)[1]
            image_path = f"uploads/{news_id}{file_extension}"
            
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            image_url = f"/uploads/{news_id}{file_extension}"
        
        # Create submission data
        submission = {
            "id": news_id,
            "news_title": title,
            "news_description": description,
            "city": city,
            "category": category,
            "publisher_name": reporter_name,
            "publisher_phone": contact_number,
            "image_path": image_url,
            "status": "pending",
            "timestamp": datetime.datetime.now()
        }
        
        # Save to database
        db_service.add_submission(submission)
        
        # Add to Google Sheets in background
        submission_obj = ProcessedSubmission(**submission)
        background_tasks.add_task(sheets_service.append_submission, submission_obj)
        
        # Format response
        response = {
            "id": news_id,
            "title": title,
            "description": description,
            "city": city,
            "category": category,
            "reporter_name": reporter_name,
            "contact_number": contact_number,
            "image_url": image_url,
            "status": "pending",
            "created_at": submission["timestamp"]
        }
        
        return response
        
    except Exception as e:
        if 'image_path' in locals() and os.path.exists(image_path):
            os.remove(image_path)  # Clean up image if there was an error
        raise HTTPException(status_code=500, detail=f"Error processing submission: {str(e)}")

@app.get("/news", response_model=List[NewsResponse])
async def get_news(
    status: Optional[str] = None,
    category: Optional[str] = None,
    city: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    """Get news items with optional filters"""
    try:
        filters = {}
        if status:
            filters["status"] = status
        if category:
            filters["category"] = category
        if city:
            filters["city"] = city
            
        news_items = db_service.get_submissions(filters, limit, offset)
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.get("/news/{news_id}", response_model=NewsResponse)
async def get_news_by_id(news_id: str):
    """Get a specific news item by ID"""
    try:
        news_item = db_service.get_submission_by_id(news_id)
        if not news_item:
            raise HTTPException(status_code=404, detail="News item not found")
        return news_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.post("/sync/manual")
async def trigger_manual_sync():
    """Manually trigger synchronization with Google Sheets"""
    try:
        result = sync_service.sync_sheets_to_db()
        return {
            "success": True,
            "message": "Manual sync completed",
            "added": result.get("added", 0),
            "skipped": result.get("skipped", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

@app.get("/sync/status")
async def get_sync_status():
    """Get the status of the sync service"""
    try:
        return {
            "running": sync_service._running,
            "last_sync_time": sync_service.last_sync_time.isoformat(),
            "database_count": db_service.count_submissions()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sync status: {str(e)}")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app", 
        host=settings.APP_HOST, 
        port=settings.APP_PORT, 
        reload=settings.DEBUG
    )
