from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.api_key import APIKeyCreate, APIKeyUpdate, APIKeyResponse, APIKeyCreateResponse
from app.services import api_key_service
from app.api.deps import get_current_user
from typing import List

router = APIRouter()

@router.post("/", response_model=APIKeyCreateResponse)
def create_api_key(
    realm_id: str = Path(..., description="The ID of the realm"),
    api_key: APIKeyCreate = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_api_key, plain_key = api_key_service.create_api_key(db, api_key, current_user["id"], realm_id)
    return APIKeyCreateResponse(
        id=db_api_key.id,
        name=db_api_key.name,
        masked=db_api_key.masked,
        is_disabled=db_api_key.is_disabled,
        disabled_at=db_api_key.disabled_at,
        value=plain_key
    )

@router.get("/", response_model=List[APIKeyResponse])
def get_user_api_keys(
    realm_id: str = Path(..., description="The ID of the realm"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        db_api_keys = api_key_service.get_user_api_keys(db, current_user["id"], realm_id)
        return [APIKeyResponse(
            id=key.id,
            name=key.name,
            masked=key.masked,
            is_disabled=key.is_disabled,
            disabled_at=key.disabled_at
        ) for key in db_api_keys]
    except HTTPException as e:
        raise e

@router.get("/{api_key_id}", response_model=APIKeyResponse)
def get_api_key(
    realm_id: str = Path(..., description="The ID of the realm"),
    api_key_id: str = Path(..., description="The ID of the API key"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_api_key = api_key_service.get_api_key(db, api_key_id, current_user["id"], realm_id)
    return APIKeyResponse(
        id=db_api_key.id,
        name=db_api_key.name,
        masked=db_api_key.masked,
        is_disabled=db_api_key.is_disabled,
        disabled_at=db_api_key.disabled_at
    )

@router.patch("/{api_key_id}", response_model=APIKeyResponse)
def update_api_key(
    realm_id: str = Path(..., description="The ID of the realm"),
    api_key_id: str = Path(..., description="The ID of the API key"),
    api_key: APIKeyUpdate = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_api_key = api_key_service.update_api_key(db, api_key_id, api_key, current_user["id"], realm_id)
    return APIKeyResponse(
        id=db_api_key.id,
        name=db_api_key.name,
        masked=db_api_key.masked,
        is_disabled=db_api_key.is_disabled,
        disabled_at=db_api_key.disabled_at
    )

@router.delete("/{api_key_id}")
def delete_api_key(
    realm_id: str = Path(..., description="The ID of the realm"),
    api_key_id: str = Path(..., description="The ID of the API key"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    api_key_service.delete_api_key(db, api_key_id, current_user["id"], realm_id)
    return {"message": "API Key deleted successfully"}
