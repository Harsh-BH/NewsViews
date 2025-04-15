from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import asyncio

# Import routers
from routers.submissions import router as submissions_router
from routers.sync import router as sync_router, get_sync_service
from utils.logger import setup_logger
from utils.config_check import print_config_status
from db.database import engine
from db import models
from utils.temp_storage import temp_storage

# Set up logger
logger = setup_logger("main")

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title="NewsViews API",
    description="API for processing news submissions from Google Forms",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(submissions_router)
app.include_router(sync_router)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to NewsViews API"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    # Check configuration status
    logger.info("Checking configuration status on startup...")
    config_status = print_config_status()
    
    # Start the temporary file cleanup thread
    logger.info("Starting temporary file cleanup thread...")
    temp_storage.start_cleanup_thread(interval_minutes=30)
    
    # Start the sync service on app startup only if Google Sheets is properly configured
    if config_status["google_sheets"]:
        logger.info("Starting sync service on application startup")
        sync_service = get_sync_service()
        sync_service.start()
    else:
        logger.warning("Sync service not started: Google Sheets integration is disabled")

@app.on_event("shutdown")
async def shutdown_event():
    # Stop the temporary file cleanup thread
    logger.info("Stopping temporary file cleanup thread...")
    temp_storage.stop_cleanup_thread()
    
    # Stop the sync service on app shutdown
    logger.info("Stopping sync service on application shutdown")
    sync_service = get_sync_service()
    if sync_service and sync_service.running:
        sync_service.stop()

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting NewsViews API server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
