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
from datetime import datetime, timezone, timedelta
import uuid

def create_bill_limit(db: Session, bill_limit: BillLimitCreate, realm_id: str) -> BillLimitResponse:
    """Create a new bill limit entry"""
    if not bill_limit.valid_from:
        raise HTTPException(
            status_code=400,
            detail="valid_from date is required"
        )
    
    valid_from = bill_limit.valid_from.astimezone(timezone.utc)

    # Find any overlapping bill limit record
    overlapping_bill_limit = (
        db.query(BillLimit)
        .filter(
            BillLimit.realm_id == realm_id,
            BillLimit.valid_from <= valid_from,
            (BillLimit.valid_to.is_(None) | (BillLimit.valid_to > valid_from))
        )
        .order_by(BillLimit.valid_from.desc())
        .first()
    )

    try:
        # If there's an overlapping record, close it the day before
        if overlapping_bill_limit:
            previous_day_end = valid_from.replace(
                hour=23, 
                minute=59, 
                second=59, 
                microsecond=999999
            ) - timedelta(days=1)

            overlapping_bill_limit.valid_to = previous_day_end
            db.add(overlapping_bill_limit)

        # Create the new bill limit record
        db_bill_limit = BillLimit(
            realm_id=realm_id,
            amount=bill_limit.amount,
            valid_from=valid_from,
            valid_to=bill_limit.valid_to
        )

        db.add(db_bill_limit)
        db.commit()
        db.refresh(db_bill_limit)
        
        return db_bill_limit

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while creating the bill limit record: {str(e)}"
        )

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

def get_bill_limit(db: Session, bill_limit_id: uuid.UUID, realm_id: str) -> BillLimit:
    """Get a specific bill limit by ID"""
    bill_limit = db.query(BillLimit).filter(
        BillLimit.id == bill_limit_id, 
        BillLimit.realm_id == realm_id
    ).first()
    
    if not bill_limit:
        raise HTTPException(status_code=404, detail="Bill limit not found")
    
    return bill_limit

def update_bill_limit(db: Session, bill_limit_id: uuid.UUID, bill_limit: BillLimitUpdate, realm_id: str) -> BillLimitResponse:
    """Update an existing bill limit"""
    current_time = datetime.now(timezone.utc)
    
    if not bill_limit.valid_from:
        raise HTTPException(
            status_code=400,
            detail="valid_from date is required"
        )
    
    valid_from = bill_limit.valid_from.astimezone(timezone.utc)
    
    # Get the existing bill limit
    existing_bill_limit = get_bill_limit(db, bill_limit_id, realm_id)
    if not existing_bill_limit:
        raise HTTPException(status_code=404, detail="Bill limit not found")

    # If it's already expired, we can't update it
    if existing_bill_limit.valid_to is not None and existing_bill_limit.valid_to < current_time:
        raise HTTPException(
            status_code=400,
            detail="Cannot update an expired bill limit entry"
        )

    try:
        # If valid_from dates match, update the existing record
        if existing_bill_limit.valid_from == valid_from:
            if bill_limit.amount is not None:
                existing_bill_limit.amount = bill_limit.amount
            if bill_limit.valid_to is not None:
                existing_bill_limit.valid_to = bill_limit.valid_to
            
            db.add(existing_bill_limit)
            db.commit()
            db.refresh(existing_bill_limit)
            return existing_bill_limit
        
        # If valid_from dates differ, create a new record
        else:
            # Close the existing bill limit
            existing_bill_limit.valid_to = valid_from.replace(
                hour=23,
                minute=59, 
                second=59, 
                microsecond=999999
            ) - timedelta(days=1)

            # Create new bill limit entry
            new_bill_limit = BillLimit(
                realm_id=realm_id,
                amount=bill_limit.amount if bill_limit.amount is not None else existing_bill_limit.amount,
                valid_from=valid_from,
                valid_to=bill_limit.valid_to
            )

            db.add(existing_bill_limit)
            db.add(new_bill_limit)
            db.commit()
            db.refresh(new_bill_limit)
            return new_bill_limit

    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def delete_bill_limit(db: Session, bill_limit_id: uuid.UUID, realm_id: str, reopen_previous_price: bool = False) -> bool:
    """
    Delete a bill limit and optionally reopen the previous price
    """
    bill_limit = get_bill_limit(db, bill_limit_id, realm_id)
    if not bill_limit:
        return False

    try:
        if reopen_previous_price:
            # Find the previous bill limit record for this realm
            previous_limit = (
                db.query(BillLimit)
                .filter(
                    BillLimit.realm_id == realm_id,
                    BillLimit.valid_from < bill_limit.valid_from,
                    BillLimit.id != bill_limit.id
                )
                .order_by(BillLimit.valid_from.desc())
                .first()
            )

            if previous_limit:
                # Reopen the previous limit by setting valid_to to None
                previous_limit.valid_to = None
                db.add(previous_limit)

        # Delete the current limit
        db.delete(bill_limit)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while deleting the bill limit: {str(e)}"
        )
