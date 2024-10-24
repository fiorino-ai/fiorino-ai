from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.overhead import OverheadCreate, OverheadUpdate, OverheadResponse
from app.services import overhead_service
from app.api.deps import get_current_user, check_realm_access
from typing import List
import uuid

router = APIRouter()

@router.post("/", response_model=OverheadResponse)
def create_overhead(
    overhead: OverheadCreate,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return overhead_service.create_overhead(db, overhead, realm.id)

@router.get("/", response_model=List[OverheadResponse])
def get_overheads(
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return overhead_service.get_overheads(db, realm.id)

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
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    overhead_service.delete_overhead(db, overhead_id, realm.id)
    return {"message": "Overhead deleted successfully"}
