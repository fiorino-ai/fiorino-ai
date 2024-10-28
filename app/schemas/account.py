from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

class AccountBase(BaseModel):
    external_id: str
    data: Optional[Dict[str, Any]] = None

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    external_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class AccountInDB(AccountBase):
    id: UUID
    realm_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AccountResponse(AccountBase):
    id: UUID
    realm_id: str

    model_config = ConfigDict(from_attributes=True) 