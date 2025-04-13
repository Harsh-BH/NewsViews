from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any

from database.database import get_db
from services.sheets_sync import sync_sheets_to_db
from api.auth import get_current_user

router = APIRouter()

@router.post("/sync/sheets", response_model=Dict[str, Any])
async def sync_sheets(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Sync Google Sheets data with database, including handling deletions
    """
    try:
        # Run in background to avoid blocking the API response
        background_tasks.add_task(sync_sheets_to_db)
        return {
            "status": "success", 
            "message": "Sync started in background. Database will be updated with changes, including deletions."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start sync: {str(e)}")
