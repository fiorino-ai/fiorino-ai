from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class LLMCostBase(BaseModel):
    provider_name: str
    llm_model_name: str
    price_per_unit: float
    unit_type: str
    overhead: float

class LLMCostCreate(LLMCostBase):
    pass

class LLMCostUpdate(BaseModel):
    price_per_unit: Optional[float] = None
    unit_type: Optional[str] = None
    overhead: Optional[float] = None

class LLMCostResponse(LLMCostBase):
    id: UUID
    valid_from: datetime
    valid_to: Optional[datetime] = None
    realm_id: str

    class Config:
        orm_mode = True

class LLMCostHistoryEntry(BaseModel):
    id: UUID
    price_per_unit: float
    unit_type: str
    overhead: float
    valid_from: datetime
    valid_to: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LLMWithCurrentCostResponse(BaseModel):
    id: UUID
    provider_name: str
    model_name: str
    price_per_unit: Optional[float] = None
    unit_type: Optional[str] = None
    overhead: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    cost_id: Optional[UUID] = None
    history: List[LLMCostHistoryEntry] = []

    model_config = ConfigDict(from_attributes=True)
