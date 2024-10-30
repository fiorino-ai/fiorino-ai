from sqlalchemy.orm import Session
from app.models.realm import Realm
from app.schemas.realm import RealmCreate, RealmUpdate, RealmResponse
from fastapi import HTTPException
from typing import List
import uuid

def get_user_realms(db: Session, user_id: str) -> List[RealmResponse]:
    realms = db.query(Realm).filter(Realm.created_by == uuid.UUID(user_id)).order_by(Realm.name).all()
    return [RealmResponse(id=realm.id, name=realm.name, bill_limit_enabled=realm.bill_limit_enabled, overhead_enabled=realm.overhead_enabled, created_at=realm.created_at) for realm in realms]

def get_realm(db: Session, realm_id: str, user_id: str) -> Realm:
    realm = db.query(Realm).filter(Realm.id == realm_id, Realm.created_by == uuid.UUID(user_id)).first()
    if not realm:
        raise HTTPException(status_code=404, detail="Realm not found")
    return realm

def create_realm(db: Session, realm: RealmCreate, user_id: str) -> RealmResponse:
    # Check if a realm with the same name already exists for this user
    existing_realm = db.query(Realm).filter(
        Realm.name == realm.name,
        Realm.created_by == uuid.UUID(user_id)
    ).first()
    if existing_realm:
        raise HTTPException(status_code=400, detail="A realm with this name already exists")

    db_realm = Realm(name=realm.name, created_by=uuid.UUID(user_id), bill_limit_enabled=realm.bill_limit_enabled, overhead_enabled=realm.overhead_enabled)
    db.add(db_realm)
    db.commit()
    db.refresh(db_realm)
    return RealmResponse(id=db_realm.id, name=db_realm.name, bill_limit_enabled=db_realm.bill_limit_enabled, overhead_enabled=db_realm.overhead_enabled, created_at=db_realm.created_at)

def update_realm(db: Session, realm_id: str, realm: RealmUpdate, user_id: str) -> RealmResponse:
    db_realm = get_realm(db, realm_id, user_id)
    
    # Check if the new name is different from the current name
    if realm.name != db_realm.name:
        # Check if a realm with the new name already exists for this user
        existing_realm = db.query(Realm).filter(
            Realm.name == realm.name,
            Realm.created_by == uuid.UUID(user_id),
            Realm.id != realm_id
        ).first()
        if existing_realm:
            raise HTTPException(status_code=400, detail="A realm with this name already exists")

    if realm.name is not None:
        db_realm.name = realm.name
    if realm.bill_limit_enabled is not None:
        db_realm.bill_limit_enabled = realm.bill_limit_enabled
    if realm.overhead_enabled is not None:
        db_realm.overhead_enabled = realm.overhead_enabled

    db.commit()
    db.refresh(db_realm)
    return RealmResponse(id=db_realm.id, name=db_realm.name, bill_limit_enabled=db_realm.bill_limit_enabled, overhead_enabled=db_realm.overhead_enabled, created_at=db_realm.created_at)

def delete_realm(db: Session, realm_id: str, user_id: str) -> None:
    db_realm = get_realm(db, realm_id, user_id)
    db.delete(db_realm)
    db.commit()
