from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.realm import RealmCreate, RealmUpdate, RealmResponse
from app.services import realm_service
from app.api.deps import get_current_user
from typing import List

router = APIRouter()

@router.get("/", response_model=List[RealmResponse])
def get_user_realms(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return realm_service.get_user_realms(db, current_user["id"])

@router.get("/{realm_id}", response_model=RealmResponse)
def get_realm(realm_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return realm_service.get_realm(db, realm_id, current_user["id"])

@router.post("/", response_model=RealmResponse)
def create_realm(realm: RealmCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return realm_service.create_realm(db, realm, current_user["id"])

@router.put("/{realm_id}", response_model=RealmResponse)
def update_realm(realm_id: str, realm: RealmUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return realm_service.update_realm(db, realm_id, realm, current_user["id"])

@router.delete("/{realm_id}")
def delete_realm(realm_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    realm_service.delete_realm(db, realm_id, current_user["id"])
    return {"message": "Realm deleted successfully"}
