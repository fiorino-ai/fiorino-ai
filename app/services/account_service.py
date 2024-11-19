from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.account import Account
from app.schemas.account import AccountUpdate, AccountResponse
from fastapi import HTTPException
from typing import List, Optional, Tuple
import uuid

def get_accounts(
    db: Session, 
    realm_id: str, 
    page: int = 1, 
    limit: int = 10, 
    search: Optional[str] = None
) -> Tuple[List[Account], int]:
    query = db.query(Account).filter(Account.realm_id == realm_id)
    
    # Apply search filter if provided
    if search:
        query = query.filter(Account.external_id.ilike(f"%{search}%"))
    
    # Get total count before pagination
    total_count = query.count()
    
    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit)
    
    return query.all(), total_count

def get_account(db: Session, account_id: uuid.UUID, realm_id: str) -> Account:
    account = db.query(Account).filter(
        Account.id == account_id,
        Account.realm_id == realm_id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

def update_account(db: Session, account_id: uuid.UUID, account: AccountUpdate, realm_id: str) -> Account:
    db_account = get_account(db, account_id, realm_id)
    
    # Update fields if provided
    if account.external_id is not None:
        db_account.external_id = account.external_id
    if account.data is not None:
        db_account.data = account.data
        
    db.commit()
    db.refresh(db_account)
    return db_account

def delete_account(db: Session, account_id: uuid.UUID, realm_id: str) -> None:
    db_account = get_account(db, account_id, realm_id)
    db.delete(db_account)
    db.commit() 