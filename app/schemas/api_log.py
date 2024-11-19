from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID

class APILogResponse(BaseModel):
    id: UUID
    path: str
    method: str
    status_code: int
    origin: Optional[str]
    request_body: Optional[Dict[str, Any]]
    response_body: Optional[Dict[str, Any]]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class APILogsResponse(BaseModel):
    logs: List[APILogResponse]
    total: int
    has_more: bool