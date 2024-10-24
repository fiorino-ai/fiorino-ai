from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class BillLimitBase(BaseModel):
    valid_from: datetime
    valid_to: Optional[datetime] = None
    amount: float

class BillLimitCreate(BillLimitBase):
    pass

class BillLimitUpdate(BaseModel):
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    amount: Optional[float] = None

class BillLimitInDB(BillLimitBase):
    id: UUID
    realm_id: str

    model_config = ConfigDict(from_attributes=True)

class BillLimitResponse(BillLimitInDB):
    pass
