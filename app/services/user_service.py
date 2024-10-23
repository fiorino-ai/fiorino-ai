from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, PasswordResetRequest, PasswordReset
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import uuid
from typing import Optional
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, password_hash=pwd_context.hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, user: UserLogin):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
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
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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
    
    user.password_hash = pwd_context.hash(new_password)
    user.reset_password_token = None
    user.reset_password_token_expiry = None
    db.commit()
    return {"message": "Password reset successful"}
