from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class APIKeyBase(BaseModel):
    name: str

class APIKeyCreate(APIKeyBase):
    realm_id: str

class APIKeyUpdate(BaseModel):
    name: Optional[str] = None
    is_disabled: Optional[bool] = None

class APIKeyResponse(APIKeyBase):
    id: UUID
    masked: str
    is_disabled: bool
    disabled_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class APIKeyCreateResponse(APIKeyResponse):
    value: str
