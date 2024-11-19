from sqlalchemy.orm import Session
from app.models.overhead import Overhead
from app.schemas.overhead import (
    OverheadCreate, 
    OverheadUpdate, 
    OverheadResponse,
    OverheadWithHistoryResponse,
    OverheadHistoryEntry
)
from fastapi import HTTPException
from typing import Optional
from datetime import datetime, timezone, timedelta
import uuid

def get_overheads(db: Session, realm_id: str) -> Optional[OverheadWithHistoryResponse]:
    """
    Get the current overhead for a realm with its history.
    Returns the current overhead and its history of changes.
    """
    current_time = datetime.now(timezone.utc)
    
    # Get all overhead records for the realm ordered by valid_from desc
    historical_records = (
        db.query(Overhead)
        .filter(Overhead.realm_id == realm_id)
        .order_by(Overhead.valid_from.desc())
        .all()
    )

    if not historical_records:
        return None

    # Get current active record (most recent valid record)
    current_record = next(
        (oh for oh in historical_records 
         if oh.valid_from <= current_time and (oh.valid_to is None or oh.valid_to > current_time)),
        None
    )

    return OverheadWithHistoryResponse(
        id=historical_records[0].id,  # Use the most recent record's ID
        percentage=current_record.percentage if current_record else None,
        valid_from=current_record.valid_from if current_record else None,
        valid_to=current_record.valid_to if current_record else None,
        realm_id=realm_id,
        history=[
            OverheadHistoryEntry(
                id=record.id,
                percentage=record.percentage,
                valid_from=record.valid_from,
                valid_to=record.valid_to
            )
            for record in historical_records
        ]
    )

def create_overhead(db: Session, overhead: OverheadCreate, realm_id: str) -> Overhead:
    """Create a new overhead entry"""
    if not overhead.valid_from:
        raise HTTPException(
            status_code=400,
            detail="valid_from date is required"
        )
    
    valid_from = overhead.valid_from.astimezone(timezone.utc)

    # Find any overlapping overhead record
    overlapping_overhead = (
        db.query(Overhead)
        .filter(
            Overhead.realm_id == realm_id,
            Overhead.valid_from <= valid_from,
            (Overhead.valid_to.is_(None) | (Overhead.valid_to > valid_from))
        )
        .order_by(Overhead.valid_from.desc())
        .first()
    )

    try:
        # If there's an overlapping record, close it the day before
        if overlapping_overhead:
            previous_day_end = valid_from.replace(
                hour=23, 
                minute=59, 
                second=59, 
                microsecond=999999
            ) - timedelta(days=1)

            overlapping_overhead.valid_to = previous_day_end
            db.add(overlapping_overhead)

        # Create the new overhead record
        db_overhead = Overhead(
            realm_id=realm_id,
            percentage=overhead.percentage,
            valid_from=valid_from,
            valid_to=overhead.valid_to
        )

        db.add(db_overhead)
        db.commit()
        db.refresh(db_overhead)
        
        return db_overhead

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while creating the overhead record: {str(e)}"
        )

def get_overhead(db: Session, overhead_id: uuid.UUID, realm_id: str) -> Overhead:
    """Get a specific overhead by ID"""
    overhead = db.query(Overhead).filter(
        Overhead.id == overhead_id, 
        Overhead.realm_id == realm_id
    ).first()
    
    if not overhead:
        raise HTTPException(status_code=404, detail="Overhead not found")
    
    return overhead

def update_overhead(db: Session, overhead_id: uuid.UUID, overhead: OverheadUpdate, realm_id: str) -> Overhead:
    """Update an existing overhead"""
    current_time = datetime.now(timezone.utc)
    valid_from = overhead.valid_from.astimezone(timezone.utc)
    
    # Get the existing overhead
    existing_overhead = get_overhead(db, overhead_id, realm_id)
    if not existing_overhead:
        return None

    # If it's already expired, we can't update it
    if existing_overhead.valid_to is not None and existing_overhead.valid_to < current_time:
        raise HTTPException(
            status_code=400,
            detail="Cannot update an expired overhead entry"
        )

    try:
        # If valid_from dates match, update the existing record
        if existing_overhead.valid_from == valid_from:
            if overhead.percentage is not None:
                existing_overhead.percentage = overhead.percentage
            if overhead.valid_to is not None:
                existing_overhead.valid_to = overhead.valid_to
            
            db.add(existing_overhead)
            db.commit()
            db.refresh(existing_overhead)
            return existing_overhead
        
        # If valid_from dates differ, create a new record
        else:
            # Close the existing overhead
            existing_overhead.valid_to = valid_from.replace(
                hour=23,
                minute=59, 
                second=59, 
                microsecond=999999
            ) - timedelta(days=1)

            # Create new overhead entry
            new_overhead = Overhead(
                realm_id=realm_id,
                percentage=overhead.percentage if overhead.percentage is not None else existing_overhead.percentage,
                valid_from=valid_from,
                valid_to=overhead.valid_to
            )

            db.add(existing_overhead)
            db.add(new_overhead)
            db.commit()
            db.refresh(new_overhead)
            return new_overhead

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def delete_overhead(db: Session, overhead_id: uuid.UUID, realm_id: str, reopen_previous_price: bool = False) -> bool:
    """
    Delete or close an overhead based on its valid_from date.
    - If valid_from is in the past: close it with current date (end of day)
    - If valid_from is in the future: delete the record
    Optionally reopen the previous price.
    """
    current_time = datetime.now(timezone.utc)
    overhead = get_overhead(db, overhead_id, realm_id)
    if not overhead:
        return False

    try:
        # Check if the overhead is from the past or future
        if overhead.valid_from <= current_time:
            # Past overhead: close it with current date at end of day
            end_of_day = current_time.replace(
                hour=23,
                minute=59,
                second=59,
                microsecond=999999
            )
            overhead.valid_to = end_of_day
            db.add(overhead)
            db.commit()
            return True
        else:
            # Future overhead: can be deleted
            if reopen_previous_price:
                # Find the previous overhead record for this realm
                previous_overhead = (
                    db.query(Overhead)
                    .filter(
                        Overhead.realm_id == realm_id,
                        Overhead.valid_from < overhead.valid_from,
                        Overhead.id != overhead.id
                    )
                    .order_by(Overhead.valid_from.desc())
                    .first()
                )

                if previous_overhead:
                    # Reopen the previous overhead by setting valid_to to None
                    previous_overhead.valid_to = None
                    db.add(previous_overhead)

            # Delete the future overhead
            db.delete(overhead)
            db.commit()
            return True

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while processing the overhead: {str(e)}"
        )
