from sqlalchemy.orm import Session
from sqlalchemy import outerjoin
from app.models.llm_cost import LLMCost
from app.models.large_language_model import LargeLanguageModel
from app.schemas.llm_cost import LLMCostCreate, LLMCostUpdate
from datetime import datetime, timezone
from fastapi import HTTPException
from typing import List
from uuid import UUID


def get_realm_llm_costs(db: Session, realm_id: str) -> List[dict]:
    """
    Get all LLMs for a realm with their current costs and cost history.
    Returns a list of LLMs with their associated cost information and history.
    """
    current_time = datetime.now(timezone.utc)
    
    # Query LLMs and their current costs (if they exist)
    results = (
        db.query(
            LargeLanguageModel,
            LLMCost
        )
        .outerjoin(
            LLMCost,
            (LargeLanguageModel.id == LLMCost.llm_id) &
            (LLMCost.valid_from <= current_time) &
            ((LLMCost.valid_to.is_(None)) | (LLMCost.valid_to > current_time))
        )
        .filter(LargeLanguageModel.realm_id == realm_id)
        .order_by(
            LargeLanguageModel.provider_name,
            LargeLanguageModel.model_name
        )
        .all()
    )

    # Format the results
    formatted_results = []
    for llm, current_cost in results:
        # Get all historical costs for this LLM
        historical_costs = (
            db.query(LLMCost)
            .filter(
                LLMCost.llm_id == llm.id,
                LLMCost.realm_id == realm_id
            )
            .order_by(LLMCost.valid_from.desc())
            .all()
        )

        result = {
            "id": llm.id,
            "provider_name": llm.provider_name,
            "model_name": llm.model_name,
            "price_per_unit": None,
            "unit_type": None,
            "overhead": None,
            "valid_from": None,
            "valid_to": None,
            "cost_id": None,
            "history": []
        }
        
        # Add current cost if it exists
        if current_cost:
            result.update({
                "price_per_unit": current_cost.price_per_unit,
                "unit_type": current_cost.unit_type,
                "overhead": current_cost.overhead,
                "valid_from": current_cost.valid_from,
                "valid_to": current_cost.valid_to,
                "cost_id": current_cost.id
            })

        # Add historical costs
        result["history"] = [
            {
                "id": cost.id,
                "price_per_unit": cost.price_per_unit,
                "unit_type": cost.unit_type,
                "overhead": cost.overhead,
                "valid_from": cost.valid_from,
                "valid_to": cost.valid_to
            }
            for cost in historical_costs
        ]
        
        formatted_results.append(result)

    return formatted_results

def get_single_llm_cost(db: Session, llm_cost_id: UUID, realm_id: str) -> LLMCost:
    """Get a specific LLM cost by ID"""
    return db.query(LLMCost).filter(
        LLMCost.id == llm_cost_id,
        LLMCost.realm_id == realm_id
    ).first()

def create_llm_cost(db: Session, llm_cost: LLMCostCreate, realm_id: str) -> LLMCost:
    """Create a new LLM cost"""
    # Check if there's an existing active cost for this provider/model
    existing_cost = db.query(LLMCost).filter(
        LLMCost.provider_name == llm_cost.provider_name,
        LLMCost.llm_model_name == llm_cost.llm_model_name,
        LLMCost.realm_id == realm_id,
        LLMCost.valid_to.is_(None)
    ).first()

    if existing_cost:
        raise HTTPException(
            status_code=400,
            detail="An active cost already exists for this provider and model"
        )

    current_time = datetime.now(timezone.utc)
    db_llm_cost = LLMCost(
        **llm_cost.dict(),
        realm_id=realm_id,
        valid_from=current_time
    )

    try:
        db.add(db_llm_cost)
        db.commit()
        db.refresh(db_llm_cost)
        return db_llm_cost
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def update_llm_cost(db: Session, llm_cost_id: UUID, llm_cost: LLMCostUpdate, realm_id: str) -> LLMCost:
    """Update an existing LLM cost"""
    current_time = datetime.now(timezone.utc)
    
    # Get the existing cost
    existing_cost = get_single_llm_cost(db, llm_cost_id, realm_id)
    if not existing_cost:
        return None

    # If it's already expired, we can't update it
    if existing_cost.valid_to is not None:
        raise HTTPException(
            status_code=400,
            detail="Cannot update an expired cost entry"
        )

    # Mark the current cost as expired
    existing_cost.valid_to = current_time

    # Create a new cost entry with the updated values
    new_cost = LLMCost(
        provider_name=existing_cost.provider_name,
        llm_model_name=existing_cost.llm_model_name,
        price_per_unit=llm_cost.price_per_unit if llm_cost.price_per_unit is not None else existing_cost.price_per_unit,
        unit_type=llm_cost.unit_type if llm_cost.unit_type is not None else existing_cost.unit_type,
        overhead=llm_cost.overhead if llm_cost.overhead is not None else existing_cost.overhead,
        valid_from=current_time,
        realm_id=realm_id
    )

    try:
        db.add(existing_cost)
        db.add(new_cost)
        db.commit()
        db.refresh(new_cost)
        return new_cost
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def delete_llm_cost(db: Session, llm_cost_id: UUID, realm_id: str) -> bool:
    """Delete an LLM cost"""
    llm_cost = get_single_llm_cost(db, llm_cost_id, realm_id)
    if not llm_cost:
        return False

    try:
        db.delete(llm_cost)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
