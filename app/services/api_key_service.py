from sqlalchemy.orm import Session
from app.models.api_key import APIKey
from app.models.realm import Realm
from app.schemas.api_key import APIKeyCreate, APIKeyUpdate
from fastapi import HTTPException
from typing import List
import uuid
import secrets
import string
from datetime import datetime, timezone

def generate_api_key():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(48))

def create_api_key(db: Session, api_key: APIKeyCreate, user_id: str) -> APIKey:
    # Check if the user is the author of the realm
    realm = db.query(Realm).filter(Realm.id == api_key.realm_id, Realm.created_by == uuid.UUID(user_id)).first()
    if not realm:
        raise HTTPException(status_code=403, detail="You don't have permission to create an API key for this realm")

    value = generate_api_key()
    masked = '*' * 43 + value[-5:]
    db_api_key = APIKey(
        user_id=uuid.UUID(user_id),
        realm_id=api_key.realm_id,
        name=api_key.name,
        value=value,
        masked=masked
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key

def get_user_api_keys(db: Session, user_id: str, realm_id: str) -> List[APIKey]:
    # Check if the user is the author of the realm
    realm = db.query(Realm).filter(Realm.id == realm_id, Realm.created_by == uuid.UUID(user_id)).first()
    if not realm:
        raise HTTPException(status_code=403, detail="You don't have permission to access this realm")
    
    return db.query(APIKey).filter(
        APIKey.user_id == uuid.UUID(user_id),
        APIKey.realm_id == realm_id
    ).all()

def get_api_key(db: Session, api_key_id: str, user_id: str) -> APIKey:
    api_key = db.query(APIKey).filter(APIKey.id == uuid.UUID(api_key_id), APIKey.user_id == uuid.UUID(user_id)).first()
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")
    return api_key

def update_api_key(db: Session, api_key_id: str, api_key: APIKeyUpdate, user_id: str) -> APIKey:
    db_api_key = get_api_key(db, api_key_id, user_id)
    if api_key.name is not None:
        db_api_key.name = api_key.name
    if api_key.is_disabled is not None:
        db_api_key.is_disabled = api_key.is_disabled
        db_api_key.disabled_at = datetime.now(timezone.utc) if api_key.is_disabled else None
    db.commit()
    db.refresh(db_api_key)
    return db_api_key

def delete_api_key(db: Session, api_key_id: str, user_id: str) -> None:
    db_api_key = get_api_key(db, api_key_id, user_id)
    db.delete(db_api_key)
    db.commit()
