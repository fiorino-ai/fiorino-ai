from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class OverheadBase(BaseModel):
    valid_from: datetime
    valid_to: Optional[datetime] = None
    percentage: float

class OverheadCreate(OverheadBase):
    pass

class OverheadUpdate(BaseModel):
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    percentage: Optional[float] = None

class OverheadInDB(OverheadBase):
    id: UUID
    realm_id: str

    model_config = ConfigDict(from_attributes=True)

class OverheadResponse(OverheadInDB):
    pass
