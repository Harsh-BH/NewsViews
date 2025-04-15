from fastapi import APIRouter, Depends, HTTPException
from services.sync_service import SyncService
from utils.logger import setup_logger
from utils.config_check import check_google_credentials, print_config_status

# Set up logger
logger = setup_logger("routers.sync")

router = APIRouter(
    prefix="/sync",
    tags=["sync"],
    responses={404: {"description": "Not found"}}
)

# Global instance of the sync service
sync_service = None

def get_sync_service():
    global sync_service
    if sync_service is None:
        # Don't auto-start, we'll control it via API
        sync_service = SyncService(interval_seconds=150, auto_start=False)
    return sync_service

@router.post("/start")
async def start_sync(
    service: SyncService = Depends(get_sync_service)
):
    """Start the synchronization service"""
    if not service.google_sheets_enabled:
        return {
            "status": "error", 
            "message": "Cannot start sync service: Google Sheets integration is disabled. Check your configuration."
        }
        
    if service.running:
        return {"status": "already_running", "message": "Sync service is already running"}
    
    service.start()
    logger.info("Sync service started via API request")
    return {"status": "started", "message": "Sync service started successfully"}

@router.post("/stop")
async def stop_sync(
    service: SyncService = Depends(get_sync_service)
):
    """Stop the synchronization service"""
    if not service.running:
        return {"status": "not_running", "message": "Sync service is not running"}
    
    service.stop()
    logger.info("Sync service stopped via API request")
    return {"status": "stopped", "message": "Sync service stopped successfully"}

@router.post("/sync-now")
async def run_sync_now(
    service: SyncService = Depends(get_sync_service)
):
    """Run a sync operation immediately"""
    if not service.google_sheets_enabled:
        return {
            "status": "error", 
            "message": "Cannot sync now: Google Sheets integration is disabled. Check your configuration."
        }
        
    try:
        logger.info("Manual sync requested via API")
        await service.sync_submissions()
        return {"status": "success", "message": "Sync operation completed successfully"}
    except Exception as e:
        logger.error(f"Manual sync failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Sync operation failed: {str(e)}")

@router.get("/status")
async def get_sync_status(
    service: SyncService = Depends(get_sync_service)
):
    """Get the current status of the sync service"""
    return service.get_status()

@router.get("/config")
async def get_config_status():
    """Get configuration status"""
    return print_config_status()
