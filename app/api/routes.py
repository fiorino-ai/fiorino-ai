from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.cost import LLMCost

router = APIRouter()

@router.get("/hello")
async def hello():
    return {"message": "Hello from Fiorino.AI"}

@router.post("/track_usage")
async def track_usage(user_id: str, model: str, input_tokens: int, output_tokens: int, db: Session = Depends(get_db)):
    # Implement usage tracking logic here
    pass

@router.get("/costs/{service}/{model}")
async def get_model_cost(service: str, model: str, db: Session = Depends(get_db)):
    cost = db.query(LLMCost).filter(LLMCost.service_name == service, LLMCost.model_name == model).first()
    if cost:
        return {
            "service": cost.service_name,
            "model": cost.model_name,
            "cost_per_1k_tokens": cost.cost_per_1k_tokens,
            "overhead": cost.overhead_percentage
        }
    return {"error": "Model not found"}
