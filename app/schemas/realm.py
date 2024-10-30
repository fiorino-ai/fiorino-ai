from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class RealmBase(BaseModel):
    name: str
    bill_limit_enabled: bool = False
    overhead_enabled: bool = False

class RealmCreate(RealmBase):
    pass

class RealmUpdate(BaseModel):
    name: Optional[str] = None
    bill_limit_enabled: Optional[bool] = None
    overhead_enabled: Optional[bool] = None

class RealmInDB(RealmBase):
    id: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RealmResponse(RealmBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
