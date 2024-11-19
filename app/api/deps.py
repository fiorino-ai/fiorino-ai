from fastapi import Depends, HTTPException, status, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.config import settings
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.realm import Realm
from typing import Optional
from fastapi import Header

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return {"id": str(user.id), "email": user.email}

async def get_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key is None:
        raise HTTPException(status_code=400, detail="X-API-Key header is missing")
    return x_api_key

def check_realm_access(realm_id: str = Path(...), current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    realm = db.query(Realm).filter(Realm.id == realm_id, Realm.created_by == current_user["id"]).first()
    if not realm:
        raise HTTPException(status_code=403, detail="You don't have access to this realm")
    return realm
