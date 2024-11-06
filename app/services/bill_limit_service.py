from sqlalchemy.orm import Session
from app.models.bill_limit import BillLimit
from app.schemas.bill_limit import (
    BillLimitCreate, 
    BillLimitUpdate, 
    BillLimitResponse,
    BillLimitWithHistoryResponse,
    BillLimitHistoryEntry
)
from fastapi import HTTPException
from typing import Optional
from datetime import datetime, timezone
import uuid

def create_bill_limit(db: Session, bill_limit: BillLimitCreate, realm_id: str) -> BillLimitResponse:
    db_bill_limit = BillLimit(**bill_limit.dict(), realm_id=realm_id)
    db.add(db_bill_limit)
    db.commit()
    db.refresh(db_bill_limit)
    return BillLimitResponse.from_orm(db_bill_limit)

def get_bill_limits(db: Session, realm_id: str) -> Optional[BillLimitWithHistoryResponse]:
    """
    Get the current bill limit for a realm with its history.
    Returns the current bill limit and its history of changes.
    """
    current_time = datetime.now(timezone.utc)
    
    # Get all bill limit records for the realm ordered by valid_from desc
    historical_records = (
        db.query(BillLimit)
        .filter(BillLimit.realm_id == realm_id)
        .order_by(BillLimit.valid_from.desc())
        .all()
    )

    if not historical_records:
        return None

    # Get current active record (most recent valid record)
    current_record = next(
        (bl for bl in historical_records 
         if bl.valid_from <= current_time and (bl.valid_to is None or bl.valid_to > current_time)),
        None
    )

    return BillLimitWithHistoryResponse(
        id=historical_records[0].id,  # Use the most recent record's ID
        amount=current_record.amount if current_record else None,
        valid_from=current_record.valid_from if current_record else None,
        valid_to=current_record.valid_to if current_record else None,
        realm_id=realm_id,
        history=[
            BillLimitHistoryEntry(
                id=record.id,
                amount=record.amount,
                valid_from=record.valid_from,
                valid_to=record.valid_to
            )
            for record in historical_records
        ]
    )

def get_bill_limit(db: Session, bill_limit_id: uuid.UUID, realm_id: str) -> BillLimitResponse:
    bill_limit = db.query(BillLimit).filter(BillLimit.id == bill_limit_id, BillLimit.realm_id == realm_id).first()
    if not bill_limit:
        raise HTTPException(status_code=404, detail="Bill limit not found")
    return BillLimitResponse.from_orm(bill_limit)

def update_bill_limit(db: Session, bill_limit_id: uuid.UUID, bill_limit: BillLimitUpdate, realm_id: str) -> BillLimitResponse:
    db_bill_limit = get_bill_limit(db, bill_limit_id, realm_id)
    for key, value in bill_limit.dict(exclude_unset=True).items():
        setattr(db_bill_limit, key, value)
    db.commit()
    db.refresh(db_bill_limit)
    return BillLimitResponse.from_orm(db_bill_limit)

def delete_bill_limit(db: Session, bill_limit_id: uuid.UUID, realm_id: str) -> None:
    db_bill_limit = get_bill_limit(db, bill_limit_id, realm_id)
    db.delete(db_bill_limit)
    db.commit()
