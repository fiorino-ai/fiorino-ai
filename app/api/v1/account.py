from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.account import AccountUpdate, AccountResponse
from app.services import account_service
from app.api.deps import get_current_user, check_realm_access
from typing import List, Optional
import uuid
from math import ceil

router = APIRouter()

@router.get("/", response_model=dict)
def get_accounts(
    realm: dict = Depends(check_realm_access),
    page: int = Query(1, gt=0, description="Page number"),
    limit: int = Query(10, gt=0, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by external_id"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    accounts, total_count = account_service.get_accounts(db, realm.id, page, limit, search)
    total_pages = ceil(total_count / limit)
    
    return {
        "data": [
            AccountResponse(
                id=account.id,
                external_id=account.external_id,
                data=account.data,
                created_at=account.created_at,
                realm_id=account.realm_id
            ) for account in accounts
        ],
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_items": total_count,
            "items_per_page": limit
        }
    }

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: uuid.UUID,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return account_service.get_account(db, account_id, realm.id)

@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: uuid.UUID,
    account: AccountUpdate,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return account_service.update_account(db, account_id, account, realm.id)

@router.delete("/{account_id}")
def delete_account(
    account_id: uuid.UUID,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    account_service.delete_account(db, account_id, realm.id)
    return {"message": "Account deleted successfully"} 