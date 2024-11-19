from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.overhead import (
    OverheadCreate, 
    OverheadUpdate, 
    OverheadResponse,
    OverheadWithHistoryResponse
)
from app.services import overhead_service
from app.api.deps import get_current_user, check_realm_access
from app.models.overhead import Overhead
from typing import Optional
import uuid
from datetime import datetime, timezone

router = APIRouter()

@router.get("/", response_model=Optional[OverheadWithHistoryResponse])
def get_overheads(
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get the current overhead with its history"""
    return overhead_service.get_overheads(db, realm.id)

@router.post("/", response_model=OverheadResponse)
def create_overhead(
    overhead: OverheadCreate,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return overhead_service.create_overhead(db, overhead, realm.id)

@router.get("/{overhead_id}", response_model=OverheadResponse)
def get_overhead(
    overhead_id: uuid.UUID,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return overhead_service.get_overhead(db, overhead_id, realm.id)

@router.put("/{overhead_id}", response_model=OverheadResponse)
def update_overhead(
    overhead_id: uuid.UUID,
    overhead: OverheadUpdate,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return overhead_service.update_overhead(db, overhead_id, overhead, realm.id)

@router.delete("/{overhead_id}")
def delete_overhead(
    overhead_id: uuid.UUID,
    reopen_previous_price: bool = Query(
        False,
        description="When true, reopens the previous price (only for future overheads)"
    ),
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    success = overhead_service.delete_overhead(db, overhead_id, realm.id, reopen_previous_price)
    if not success:
        raise HTTPException(status_code=404, detail="Overhead not found")
    
    current_time = datetime.now(timezone.utc)
    overhead = db.query(Overhead).get(overhead_id)
    
    if overhead and overhead.valid_from <= current_time:
        message = "Overhead closed with current date"
    else:
        message = "Overhead deleted successfully"
        if reopen_previous_price:
            message += " and previous price reopened"
    
    return {"message": message}
