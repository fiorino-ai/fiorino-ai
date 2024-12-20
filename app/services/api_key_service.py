from sqlalchemy.orm import Session
from app.models.api_key import APIKey
from app.models.realm import Realm
from app.schemas.api_key import APIKeyCreate, APIKeyUpdate
from fastapi import HTTPException
from typing import List, Optional, Tuple
import uuid
import secrets
import string
from datetime import datetime, timezone
import hashlib

def generate_api_key() -> Tuple[str, str]:
    plain_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(48))
    hashed_key = hashlib.sha256(plain_key.encode()).hexdigest()
    return plain_key, hashed_key

def create_api_key(db: Session, api_key: APIKeyCreate, user_id: str, realm_id: str) -> Tuple[APIKey, str]:
    realm = db.query(Realm).filter(Realm.id == realm_id, Realm.created_by == uuid.UUID(user_id)).first()
    if not realm:
        raise HTTPException(status_code=403, detail="You don't have permission to create an API key for this realm")

    plain_key, hashed_key = generate_api_key()
    masked = '*' * 43 + plain_key[-5:]
    db_api_key = APIKey(
        user_id=uuid.UUID(user_id),
        realm_id=realm_id,
        name=api_key.name,
        value=hashed_key,
        masked=masked
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key, plain_key

def get_user_api_keys(db: Session, user_id: str, realm_id: str) -> List[APIKey]:
    realm = db.query(Realm).filter(Realm.id == realm_id, Realm.created_by == uuid.UUID(user_id)).first()
    if not realm:
        raise HTTPException(status_code=403, detail="You don't have permission to access this realm")
    
    return db.query(APIKey).filter(
        APIKey.user_id == uuid.UUID(user_id),
        APIKey.realm_id == realm_id
    ).all()

def get_api_key(db: Session, api_key_id: str, user_id: str, realm_id: str) -> APIKey:
    api_key = db.query(APIKey).filter(
        APIKey.id == uuid.UUID(api_key_id),
        APIKey.user_id == uuid.UUID(user_id),
        APIKey.realm_id == realm_id
    ).first()
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")
    return api_key

def update_api_key(db: Session, api_key_id: str, api_key: APIKeyUpdate, user_id: str, realm_id: str) -> APIKey:
    db_api_key = get_api_key(db, api_key_id, user_id, realm_id)
    if api_key.name is not None:
        db_api_key.name = api_key.name
    if api_key.is_disabled is not None:
        db_api_key.is_disabled = api_key.is_disabled
        db_api_key.disabled_at = datetime.now(timezone.utc) if api_key.is_disabled else None
    db.commit()
    db.refresh(db_api_key)
    return db_api_key

def delete_api_key(db: Session, api_key_id: str, user_id: str, realm_id: str) -> None:
    db_api_key = get_api_key(db, api_key_id, user_id, realm_id)
    db.delete(db_api_key)
    db.commit()

def validate_api_key(db: Session, plain_api_key: str) -> Optional[APIKey]:
    hashed_key = hashlib.sha256(plain_api_key.encode()).hexdigest()
    return db.query(APIKey).filter(APIKey.value == hashed_key, APIKey.is_disabled == False).first()
