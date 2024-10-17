from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsageCreate(BaseModel):
    user_id: str
    provider_name: str
    llm_model_name: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    message: Optional[str] = None

class UsageResponse(BaseModel):
    id: int
    user_id: str
    llm_cost_id: int
    input_tokens: int
    output_tokens: int
    total_tokens: int
    total_model_price: float
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True
