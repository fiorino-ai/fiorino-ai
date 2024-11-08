from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from uuid import UUID

class OverheadBase(BaseModel):
    percentage: float
    valid_from: datetime
    valid_to: Optional[datetime] = None

class OverheadCreate(OverheadBase):
    pass

class OverheadUpdate(BaseModel):
    percentage: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

class OverheadResponse(BaseModel):
    id: UUID
    percentage: float
    valid_from: datetime
    valid_to: Optional[datetime] = None
    realm_id: str

    model_config = ConfigDict(from_attributes=True)

class OverheadHistoryEntry(BaseModel):
    id: UUID
    percentage: float
    valid_from: datetime
    valid_to: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class OverheadWithHistoryResponse(BaseModel):
    id: UUID
    percentage: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    realm_id: str
    history: List[OverheadHistoryEntry] = []

    model_config = ConfigDict(from_attributes=True)
