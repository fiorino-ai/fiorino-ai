from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class RealmBase(BaseModel):
    name: str

class RealmCreate(RealmBase):
    pass

class RealmUpdate(RealmBase):
    pass

class RealmInDB(RealmBase):
    id: str
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RealmResponse(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)
