from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class LLMCostBase(BaseModel):
    price_per_unit: float
    unit_type: str
    overhead: float
    valid_from: datetime

class LLMCostCreate(LLMCostBase):
    provider_name: str
    model_name: str

class LLMCostUpdate(BaseModel):
    valid_from: datetime
    price_per_unit: Optional[float] = None
    unit_type: Optional[str] = None
    overhead: Optional[float] = None

class LLMCostResponse(BaseModel):
    id: UUID
    llm_id: UUID
    price_per_unit: float
    unit_type: str
    overhead: float
    valid_from: datetime
    valid_to: Optional[datetime] = None
    realm_id: str

    model_config = ConfigDict(from_attributes=True)

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
