from sqlalchemy.orm import Session
from app.models.overhead import Overhead
from app.schemas.overhead import OverheadCreate, OverheadUpdate, OverheadResponse
from fastapi import HTTPException
from typing import List
import uuid

def create_overhead(db: Session, overhead: OverheadCreate, realm_id: str) -> OverheadResponse:
    db_overhead = Overhead(**overhead.dict(), realm_id=realm_id)
    db.add(db_overhead)
    db.commit()
    db.refresh(db_overhead)
    return OverheadResponse.from_orm(db_overhead)

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
