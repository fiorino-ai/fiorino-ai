from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.llm_cost import LLMCost
from app.schemas.llm_cost import (
    LLMCostCreate, 
    LLMCostUpdate, 
    LLMCostResponse, 
    LLMWithCurrentCostResponse
)
from datetime import datetime
from app.services.llm_cost_service import (
    get_realm_llm_costs,
    get_single_llm_cost,
    create_llm_cost,
    update_llm_cost,
    delete_llm_cost
)
from app.api.deps import get_current_user, check_realm_access
from typing import List
from uuid import UUID

router = APIRouter()

@router.get("/", response_model=List[LLMWithCurrentCostResponse])
async def get_llm_costs(
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all LLMs for a realm with their current costs if they exist"""
    return get_realm_llm_costs(db, realm.id)

@router.get("/{llm_cost_id}", response_model=LLMCostResponse)
async def get_llm_cost(
    llm_cost_id: UUID,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific LLM cost by ID"""
    cost = get_single_llm_cost(db, llm_cost_id, realm.id)
    if not cost:
        raise HTTPException(status_code=404, detail="LLM cost not found")
    return cost

@router.post("/", response_model=LLMCostResponse)
async def create_new_llm_cost(
    llm_cost: LLMCostCreate,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new LLM cost"""
    return create_llm_cost(db, llm_cost, realm.id)

@router.put("/{llm_cost_id}", response_model=LLMCostResponse)
async def update_llm_cost_by_id(
    llm_cost_id: UUID,
    llm_cost: LLMCostUpdate,
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update an existing LLM cost"""
    updated_cost = update_llm_cost(db, llm_cost_id, llm_cost, realm.id)
    if not updated_cost:
        raise HTTPException(status_code=404, detail="LLM cost not found")
    return updated_cost

@router.delete("/{llm_cost_id}")
async def delete_llm_cost_by_id(
    llm_cost_id: UUID,
    reopen_previous_price: bool = Query(
        False,
        description="When true, reopens the previous price for this LLM"
    ),
    realm: dict = Depends(check_realm_access),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an LLM cost.
    Optionally reopen the previous price for this LLM if reopen_previous_price is True.
    """
    success = delete_llm_cost(db, llm_cost_id, realm.id, reopen_previous_price)
    if not success:
        raise HTTPException(status_code=404, detail="LLM cost not found")
    
    message = "LLM cost deleted successfully"
    if reopen_previous_price:
        message += " and previous price reopened"
    
    return {"message": message}

