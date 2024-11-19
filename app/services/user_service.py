from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
import uuid
from typing import Optional
from jose import jwt
from app.core.security import get_password_hash, verify_password
from app.core.config import settings

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, password_hash=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, user: UserLogin):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at
    }

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def request_password_reset(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = str(uuid.uuid4())
    user.reset_password_token = token
    user.reset_password_token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    db.commit()
    
    # TODO: Send email with reset link
    # Here you would typically send an email with the reset link
    # For this example, we'll just return the token
    return token

def reset_password(db: Session, token: str, new_password: str):
    user = db.query(User).filter(User.reset_password_token == token).first()
    if not user or user.reset_password_token_expiry < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user.password_hash = get_password_hash(new_password)
    user.reset_password_token = None
    user.reset_password_token_expiry = None
    db.commit()
    return {"message": "Password reset successful"}
