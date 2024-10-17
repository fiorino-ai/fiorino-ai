from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.llmcost import LLMCost
from datetime import datetime

router = APIRouter()

@router.get("/hello")
async def hello():
    return {"message": "Hello from Fiorino.AI"}

@router.post("/track_usage")
async def track_usage(user_id: str, model: str, input_tokens: int, output_tokens: int, db: Session = Depends(get_db)):
    # Implement usage tracking logic here
    pass

@router.get("/costs/{provider}/{model}")
async def get_model_cost(provider: str, model: str, db: Session = Depends(get_db)):
    current_time = datetime.utcnow()
    cost = db.query(LLMCost).filter(
        LLMCost.provider_name == provider,
        LLMCost.model_name == model,
        LLMCost.valid_from <= current_time,
        (LLMCost.valid_to.is_(None) | (LLMCost.valid_to > current_time))
    ).order_by(LLMCost.valid_from.desc()).first()

    if cost:
        return {
            "provider": cost.provider_name,
            "model": cost.model_name,
            "price_per_unit": cost.price_per_unit,
            "unit_type": cost.unit_type,
            "overhead": cost.overhead_percentage
        }
    raise HTTPException(status_code=404, detail="Model cost not found")
