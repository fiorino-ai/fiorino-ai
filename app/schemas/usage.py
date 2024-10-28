from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class UsageCreate(BaseModel):
    user_id: str
    provider_name: str
    llm_model_name: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    message: Optional[str] = None
    realm_id: Optional[str] = None
    api_key_id: Optional[UUID] = None

class UsageResponse(BaseModel):
    id: int
    user_id: str
    realm_id: str
    api_key_id: Optional[UUID]
    llm_cost_id: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    total_model_price: float
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True
