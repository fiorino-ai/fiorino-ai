from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, PasswordResetRequest, PasswordReset
from app.services import user_service
from datetime import timedelta

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # TODO: do not return created_at and updated_at 
    return user_service.create_user(db, user)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_service.authenticate_user(db, user)
    access_token_expires = timedelta(minutes=user_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/password-reset-request")
def password_reset_request(request: PasswordResetRequest, db: Session = Depends(get_db)):
    token = user_service.request_password_reset(db, request.email)
    return {"message": "Password reset token generated", "token": token}

@router.post("/password-reset")
def password_reset(reset: PasswordReset, db: Session = Depends(get_db)):
    return user_service.reset_password(db, reset.token, reset.new_password)
