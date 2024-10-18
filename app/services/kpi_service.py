from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models.usage import Usage
from app.models.llm_cost import LLMCost
from typing import Optional, List, Dict

def get_daily_costs(db: Session, start_date: date, end_date: date, user_id: Optional[str] = None) -> List[Dict]:
    query = db.query(
        func.date(Usage.created_at).label('date'),
        LLMCost.provider_name,
        LLMCost.llm_model_name,
        func.sum(Usage.total_price).label('total_cost')
    ).join(LLMCost, Usage.llm_cost_id == LLMCost.id)
    
    query = apply_date_and_user_filter(query, start_date, end_date, user_id)
    
    query = query.group_by(
        func.date(Usage.created_at),
        LLMCost.provider_name,
        LLMCost.llm_model_name
    ).order_by(func.date(Usage.created_at))
    
    results = query.all()
    
    return [
        {
            'date': result.date,
            'provider_name': result.provider_name,
            'llm_model_name': result.llm_model_name,
            'total_cost': float(result.total_cost)
        }
        for result in results
    ]

def get_total_cost(db: Session, start_date: date, end_date: date, user_id: Optional[str] = None) -> float:
    query = db.query(func.sum(Usage.total_model_price).label('total_cost'))
    query = apply_date_and_user_filter(query, start_date, end_date, user_id)
    result = query.scalar()
    return float(result) if result else 0.0

def get_total_usage_fees(db: Session, start_date: date, end_date: date, user_id: Optional[str] = None) -> float:
    query = db.query(
        (func.sum(Usage.total_price) - func.sum(Usage.total_model_price)).label('total_usage_fees')
    )
    query = apply_date_and_user_filter(query, start_date, end_date, user_id)
    result = query.scalar()
    return float(result) if result else 0.0

def get_most_used_models(db: Session, start_date: date, end_date: date, user_id: Optional[str] = None) -> List[Dict]:
    query = db.query(
        LLMCost.provider_name,
        LLMCost.llm_model_name,
        func.sum(Usage.total_tokens).label('total_tokens'),
        func.sum(Usage.total_model_price).label('total_model_price')
    ).join(LLMCost, Usage.llm_cost_id == LLMCost.id)
    
    query = apply_date_and_user_filter(query, start_date, end_date, user_id)
    
    query = query.group_by(
        LLMCost.provider_name,
        LLMCost.llm_model_name
    ).order_by(func.sum(Usage.total_tokens).desc())
    
    results = query.all()
    
    return [
        {
            'provider_name': result.provider_name,
            'llm_model_name': result.llm_model_name,
            'total_tokens': int(result.total_tokens),
            'total_model_price': float(result.total_model_price)
        }
        for result in results
    ]

def get_model_costs(db: Session, start_date: date, end_date: date, user_id: Optional[str] = None) -> List[Dict]:
    query = db.query(
        LLMCost.provider_name,
        LLMCost.llm_model_name,
        func.date(Usage.created_at).label('date'),
        func.sum(Usage.total_model_price).label('daily_cost')
    ).join(LLMCost, Usage.llm_cost_id == LLMCost.id)
    
    query = apply_date_and_user_filter(query, start_date, end_date, user_id)
    
    query = query.group_by(
        LLMCost.provider_name,
        LLMCost.llm_model_name,
        func.date(Usage.created_at)
    ).order_by(
        LLMCost.provider_name,
        LLMCost.llm_model_name,
        func.date(Usage.created_at)
    )
    
    results = query.all()
    
    model_costs = {}
    for result in results:
        model_key = f"{result.provider_name}:{result.llm_model_name}"
        if model_key not in model_costs:
            model_costs[model_key] = {
                'provider_name': result.provider_name,
                'llm_model_name': result.llm_model_name,
                'daily_costs': []
            }
        model_costs[model_key]['daily_costs'].append({
            'date': result.date,
            'cost': float(result.daily_cost)
        })
    
    return list(model_costs.values())

def apply_date_and_user_filter(query, start_date: date, end_date: date, user_id: Optional[str] = None):
    query = query.filter(func.date(Usage.created_at) >= start_date, func.date(Usage.created_at) <= end_date)
    if user_id:
        query = query.filter(Usage.user_id == user_id)
    return query
