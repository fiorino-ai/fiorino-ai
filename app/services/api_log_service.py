from sqlalchemy.orm import Session
from app.models.api_log import APILog
from fastapi import Request, Response, HTTPException
from typing import List, Optional, Tuple
from datetime import datetime
import json

async def log_api_request(
    db: Session,
    request: Request,
    response: Response,
    realm_id: str,
    status_code: int,
    response_body: dict
) -> APILog:
    # Get request body
    try:
        body_bytes = await request.body()
        request_body = json.loads(body_bytes) if body_bytes else None
    except:
        request_body = None

    # Create log entry
    log = APILog(
        realm_id=realm_id,
        path=str(request.url.path),
        method=request.method,
        status_code=status_code,
        origin=request.headers.get('origin'),
        request_body=request_body,
        response_body=response_body
    )

    db.add(log)
    db.commit()
    db.refresh(log)
    return log 

def get_api_logs(
    db: Session,
    realm_id: str,
    skip: int = 0,
    limit: int = 20,
    status_code: Optional[int] = None
) -> Tuple[List[APILog], int]:
    """
    Get API logs with offset pagination and optional status filter.
    Returns tuple of (logs, total_count).
    """
    # Base query
    query = db.query(APILog).filter(APILog.realm_id == realm_id)

    # Apply status code filter if provided
    if status_code:
        query = query.filter(APILog.status_code == status_code)

    # Get total count before pagination
    total_count = query.count()

    # Apply pagination and ordering
    logs = query.order_by(APILog.created_at.desc())\
               .offset(skip)\
               .limit(limit)\
               .all()

    return logs, total_count

def delete_logs_before_date(db: Session, realm_id: str, before_date: datetime) -> int:
    """
    Delete all logs before a given date for a realm.
    Returns the number of deleted logs.
    """
    try:
        deleted_count = db.query(APILog).filter(
            APILog.realm_id == realm_id,
            APILog.created_at < before_date
        ).delete()
        
        db.commit()
        return deleted_count
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting logs: {str(e)}"
        ) 