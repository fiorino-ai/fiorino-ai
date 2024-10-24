from sqlalchemy.orm import Session
from app.models.bill_limit import BillLimit
from app.schemas.bill_limit import BillLimitCreate, BillLimitUpdate, BillLimitResponse
from fastapi import HTTPException
from typing import List
import uuid

def create_bill_limit(db: Session, bill_limit: BillLimitCreate, realm_id: str) -> BillLimitResponse:
    db_bill_limit = BillLimit(**bill_limit.dict(), realm_id=realm_id)
    db.add(db_bill_limit)
    db.commit()
    db.refresh(db_bill_limit)
    return BillLimitResponse.from_orm(db_bill_limit)

def get_bill_limits(db: Session, realm_id: str) -> List[BillLimitResponse]:
    bill_limits = db.query(BillLimit).filter(BillLimit.realm_id == realm_id).all()
    return [BillLimitResponse.from_orm(bl) for bl in bill_limits]

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
