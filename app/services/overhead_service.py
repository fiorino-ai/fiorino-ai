from sqlalchemy.orm import Session
from app.models.overhead import Overhead
from app.schemas.overhead import OverheadCreate, OverheadUpdate, OverheadResponse
from fastapi import HTTPException
from typing import List
from datetime import datetime, timezone, timedelta
import uuid

def create_overhead(db: Session, overhead: OverheadCreate, realm_id: str) -> OverheadResponse:
    """Create a new overhead entry"""
    # Ensure valid_from is provided and convert to UTC
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
            # Set the end of the previous day as the valid_to
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
        return OverheadResponse.from_orm(db_overhead)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while creating the overhead record: {str(e)}"
        )

def get_overheads(db: Session, realm_id: str) -> List[OverheadResponse]:
    overheads = db.query(Overhead).filter(Overhead.realm_id == realm_id).all()
    return [OverheadResponse.from_orm(oh) for oh in overheads]

def get_overhead(db: Session, overhead_id: uuid.UUID, realm_id: str) -> OverheadResponse:
    overhead = db.query(Overhead).filter(Overhead.id == overhead_id, Overhead.realm_id == realm_id).first()
    if not overhead:
        raise HTTPException(status_code=404, detail="Overhead not found")
    return OverheadResponse.from_orm(overhead)

def update_overhead(db: Session, overhead_id: uuid.UUID, overhead: OverheadUpdate, realm_id: str) -> OverheadResponse:
    db_overhead = get_overhead(db, overhead_id, realm_id)
    for key, value in overhead.dict(exclude_unset=True).items():
        setattr(db_overhead, key, value)
    db.commit()
    db.refresh(db_overhead)
    return OverheadResponse.from_orm(db_overhead)

def delete_overhead(db: Session, overhead_id: uuid.UUID, realm_id: str) -> None:
    db_overhead = get_overhead(db, overhead_id, realm_id)
    db.delete(db_overhead)
    db.commit()
