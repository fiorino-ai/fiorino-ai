from sqlalchemy.orm import Session
from app.models.llm_cost import LLMCost
from datetime import datetime, timezone
from fastapi import HTTPException

def add_or_update_llm_cost(
    db: Session,
    provider_name: str,
    model_name: str,
    price_per_unit: float = None,
    unit_type: str = None,
    overhead_percentage: float = None
):
    current_time = datetime.now(timezone.utc)

    existing_cost = db.query(LLMCost).filter(
        LLMCost.provider_name == provider_name,
        LLMCost.model_name == model_name,
        LLMCost.valid_to.is_(None)
    ).first()

    if existing_cost:
        existing_cost.valid_to = current_time
        db.add(existing_cost)

        new_cost = LLMCost(
            provider_name=provider_name,
            model_name=model_name,
            price_per_unit=price_per_unit if price_per_unit is not None else existing_cost.price_per_unit,
            unit_type=unit_type if unit_type is not None else existing_cost.unit_type,
            overhead_percentage=overhead_percentage if overhead_percentage is not None else existing_cost.overhead_percentage,
            valid_from=current_time
        )
    else:
        if price_per_unit is None or unit_type is None or overhead_percentage is None:
            raise HTTPException(status_code=400, detail="All fields are required when creating a new cost entry")
        new_cost = LLMCost(
            provider_name=provider_name,
            model_name=model_name,
            price_per_unit=price_per_unit,
            unit_type=unit_type,
            overhead_percentage=overhead_percentage,
            valid_from=current_time
        )

    db.add(new_cost)

    try:
        db.commit()
        return new_cost
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the database: {str(e)}")
