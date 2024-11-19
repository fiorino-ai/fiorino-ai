from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.bill_limit import (
    BillLimitCreate, 
    BillLimitUpdate, 
    BillLimitResponse,
    BillLimitWithHistoryResponse
)
from app.services import bill_limit_service
from app.api.deps import get_current_user, check_realm_access
from typing import Optional
import uuid

router = APIRouter()

@router.post("/", response_model=BillLimitResponse)
def create_bill_limit(
    bill_limit: BillLimitCreate,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return bill_limit_service.create_bill_limit(db, bill_limit, realm.id)

@router.get("/", response_model=Optional[BillLimitWithHistoryResponse])
def get_bill_limits(
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get the current bill limit with its history"""
    return bill_limit_service.get_bill_limits(db, realm.id)

@router.get("/{bill_limit_id}", response_model=BillLimitResponse)
def get_bill_limit(
    bill_limit_id: uuid.UUID,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return bill_limit_service.get_bill_limit(db, bill_limit_id, realm.id)

@router.put("/{bill_limit_id}", response_model=BillLimitResponse)
def update_bill_limit(
    bill_limit_id: uuid.UUID,
    bill_limit: BillLimitUpdate,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a bill limit"""
    result = bill_limit_service.update_bill_limit(db, bill_limit_id, bill_limit, realm.id)
    if not result:
        raise HTTPException(status_code=404, detail="Bill limit not found")
    return result

@router.delete("/{bill_limit_id}")
def delete_bill_limit(
    bill_limit_id: uuid.UUID,
    reopen_previous_price: bool = Query(
        False,
        description="When true, reopens the previous price for this bill limit"
    ),
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    success = bill_limit_service.delete_bill_limit(db, bill_limit_id, realm.id, reopen_previous_price)
    if not success:
        raise HTTPException(status_code=404, detail="Bill limit not found")
    
    message = "Bill limit deleted successfully"
    if reopen_previous_price:
        message += " and previous price reopened"
    
    return {"message": message}
