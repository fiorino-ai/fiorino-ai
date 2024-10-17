from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    id: int
    valid_from: datetime
    valid_to: Optional[datetime] = None

    class Config:
        orm_mode = True
