from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.llm_cost import LLMCost
from app.schemas.llm_cost import LLMCostUpdate, LLMCostResponse
from datetime import datetime
from app.services.llm_cost_service import add_or_update_llm_cost

router = APIRouter()

@router.get("/hello")
async def hello():
    return {"message": "Hello from Fiorino.AI"}

@router.post("/track_usage")
async def track_usage(user_id: str, model: str, input_tokens: int, output_tokens: int, db: Session = Depends(get_db)):
    # Implement usage tracking logic here
    pass

@router.get("/costs/{provider}/{model}", response_model=LLMCostResponse)
async def get_model_cost(provider: str, model: str, db: Session = Depends(get_db)):
    current_time = datetime.utcnow()
    cost = db.query(LLMCost).filter(
        LLMCost.provider_name == provider,
        LLMCost.model_name == model,
        LLMCost.valid_from <= current_time,
        (LLMCost.valid_to.is_(None) | (LLMCost.valid_to > current_time))
    ).order_by(LLMCost.valid_from.desc()).first()

    if cost:
        return cost
    raise HTTPException(status_code=404, detail="Model cost not found")

@router.post("/costs/{provider}/{model}", response_model=LLMCostResponse)
async def update_model_cost(provider: str, model: str, cost_update: LLMCostUpdate, db: Session = Depends(get_db)):
    try:
        new_cost = add_or_update_llm_cost(
            db,
            provider,
            model,
            cost_update.price_per_unit,
            cost_update.unit_type,
            cost_update.overhead_percentage
        )
        return new_cost
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
