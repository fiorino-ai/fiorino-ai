from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.api_log import APILogsResponse
from app.services import api_log_service
from app.api.deps import get_current_user, check_realm_access
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.get("/logs", response_model=APILogsResponse)
async def get_logs(
    realm: dict = Depends(check_realm_access),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    status_code: Optional[int] = Query(None, description="Filter by HTTP status code"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get API logs with offset pagination and optional status filter.
    """
    logs, total_count = api_log_service.get_api_logs(
        db, realm.id, skip, limit, status_code
    )
    
    return APILogsResponse(
        logs=logs,
        total=total_count,
        has_more=(skip + limit) < total_count
    )

@router.delete("/logs")
async def delete_logs(
    before_date: datetime = Query(..., description="Delete logs before this date"),
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete all logs before a given date.
    """
    deleted_count = api_log_service.delete_logs_before_date(
        db, realm.id, before_date
    )
    
    return {
        "message": f"Successfully deleted {deleted_count} logs",
        "deleted_count": deleted_count
    } 