from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class BillLimitBase(BaseModel):
    amount: float
    valid_from: datetime
    valid_to: Optional[datetime] = None

class BillLimitCreate(BillLimitBase):
    pass

class BillLimitUpdate(BaseModel):
    amount: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

class BillLimitHistoryEntry(BaseModel):
    id: UUID
    amount: float
    valid_from: datetime
    valid_to: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class BillLimitResponse(BaseModel):
    id: UUID
    amount: float
    valid_from: datetime
    valid_to: Optional[datetime] = None
    realm_id: str

    model_config = ConfigDict(from_attributes=True)

class BillLimitWithHistoryResponse(BaseModel):
    id: UUID
    amount: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    realm_id: str
    history: List[BillLimitHistoryEntry] = []

    model_config = ConfigDict(from_attributes=True)
