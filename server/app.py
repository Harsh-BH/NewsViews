from fastapi import FastAPI, File, UploadFile, Depends, Form, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid
import datetime
import shutil
from typing import List, Optional
from pydantic import BaseModel

# Import from the consolidated config
from config import settings, UPLOAD_DIR

from models.news import NewsSubmission, ProcessedSubmission
from services.google_sheets import GoogleSheetsService
from services.duplicate_check import DuplicateCheckService
from services.database import DatabaseService
from services.form_sync_service import FormSyncService

app = FastAPI(
    title=settings.APP_NAME,
    description="API for NewsViews application",
    version=settings.APP_VERSION
)

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

# Initialize services
sheets_service = GoogleSheetsService()
duplicate_service = DuplicateCheckService()
db_service = DatabaseService()

# Setup form sync service
form_sync_service = FormSyncService()


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


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    # Start the form sync service in background
    try:
        from threading import Thread
        sync_thread = Thread(
            target=form_sync_service.start_sync_loop,
            kwargs={"interval_minutes": settings.FORM_SYNC_INTERVAL_MINUTES},
            daemon=True
        )
        sync_thread.start()
        app.state.sync_thread = sync_thread
    except Exception as e:
        print(f"Error starting form sync service: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    # Any cleanup code here
    pass


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
        
        # Create news submission object
        news_submission = NewsSubmission(
            id=news_id,
            title=title,
            description=description,
            city=city,
            category=category,
            reporter_name=reporter_name,
            contact_number=contact_number,
            image_url=image_url,
            created_at=datetime.datetime.now()
        )
        
        # Check for duplicates
        is_duplicate = duplicate_service.check_duplicate(news_submission)
        if is_duplicate:
            if image_url:
                # Remove uploaded image if duplicate
                os.remove(image_path)
            raise HTTPException(status_code=400, detail="This news appears to be a duplicate")
        
        # Process and store the submission
        processed_submission = ProcessedSubmission(
            **news_submission.dict(),
            status="pending"
        )
        
        # Save to database
        db_service.save_submission(processed_submission)
        
        # Add to Google Sheet in background
        background_tasks.add_task(
            sheets_service.append_submission,
            processed_submission
        )
        
        return processed_submission
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing submission: {str(e)}")


@app.get("/news", response_model=List[NewsResponse])
async def get_news(
    status: Optional[str] = None,
    category: Optional[str] = None,
    city: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    """
    Get news items with optional filters
    """
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
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@app.post("/sync/form")
async def trigger_form_sync():
    """Manually trigger Google Form sync"""
    try:
        items_count = form_sync_service.sync()
        return {"message": f"Form sync completed successfully", "items_processed": items_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error syncing form data: {str(e)}")


@app.get("/sync/status")
async def get_sync_status():
    """Get the status of the form sync service"""
    try:
        is_running = hasattr(app.state, "sync_thread") and app.state.sync_thread.is_alive()
        last_sync_row = form_sync_service.last_sync_row
        return {
            "is_running": is_running,
            "last_sync_row": last_sync_row,
            "spreadsheet_id": form_sync_service.spreadsheet_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sync status: {str(e)}")


# Add this endpoint after the existing sync endpoints

@app.get("/debug/form-sync")
async def debug_form_sync():
    """Debug endpoint to test form sync"""
    try:
        # Manually sync forms
        count = form_sync_service.sync()
        
        # Get the latest submissions
        news_items = db_service.get_submissions({}, limit=10, offset=0)
        
        return {
            "success": True,
            "items_processed": count,
            "last_sync_row": form_sync_service.last_sync_row,
            "latest_items": news_items
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Add this to your debug endpoints

@app.get("/debug/google-sheets")
async def debug_google_sheets():
    """Debug endpoint to check Google Sheets service status"""
    try:
        # Get Google Sheets info
        credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS
        credentials_exist = os.path.exists(credentials_path)
        
        # Check if service is initialized
        service_initialized = hasattr(sheets_service, 'service') and sheets_service.service is not None
        
        # Try a simple operation if service is initialized
        test_result = None
        error_message = None
        
        if service_initialized:
            try:
                # Just get metadata for the spreadsheet
                spreadsheet_id = settings.GOOGLE_SHEET_ID or settings.FORM_RESPONSES_SHEET_ID
                if spreadsheet_id:
                    result = sheets_service.service.spreadsheets().get(
                        spreadsheetId=spreadsheet_id
                    ).execute()
                    test_result = {
                        "title": result.get('properties', {}).get('title'),
                        "sheets": len(result.get('sheets', [])),
                        "spreadsheetId": result.get('spreadsheetId')
                    }
            except Exception as e:
                error_message = str(e)
        
        return {
            "service_initialized": service_initialized,
            "credentials_path": credentials_path,
            "credentials_exist": credentials_exist,
            "spreadsheet_id_setting": settings.GOOGLE_SHEET_ID,
            "form_responses_sheet_id": settings.FORM_RESPONSES_SHEET_ID,
            "test_result": test_result,
            "error_message": error_message
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# Add this to your debug endpoints

@app.get("/debug/database")
async def debug_database():
    """Debug endpoint to check database connectivity and content"""
    try:
        # Create a test submission
        test_id = f"test-{uuid.uuid4()}"
        test_submission = ProcessedSubmission(
            id=test_id,
            news_title="Test Title",
            news_description="This is a test submission to verify database connectivity",
            city="Test City",
            category="Test",
            publisher_name="Tester",
            publisher_phone="123-456-7890",
            image_path=None,
            status="test",
            timestamp=datetime.datetime.now()
        )
        
        # Try to save it
        db_service.save_submission(test_submission)
        
        # Try to retrieve it
        saved_submission = db_service.get_submission_by_id(test_id)
        
        # Get all submissions
        all_submissions = db_service.get_submissions({}, 100, 0)
        
        return {
            "status": "success",
            "database_url": settings.DATABASE_URL.replace(settings.DATABASE_PASSWORD, "********") if hasattr(settings, "DATABASE_PASSWORD") else settings.DATABASE_URL,
            "database_path": getattr(settings, "DATABASE_PATH", "Not set"),
            "test_submission_saved": saved_submission is not None,
            "total_submissions": len(all_submissions),
            "latest_submissions": all_submissions[:5] if all_submissions else []
        }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "database_url": settings.DATABASE_URL.replace(settings.DATABASE_PASSWORD, "********") if hasattr(settings, "DATABASE_PASSWORD") else settings.DATABASE_URL,
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app", 
        host=settings.APP_HOST, 
        port=settings.APP_PORT, 
        reload=settings.DEBUG
    )
