from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models.usage import Usage
from app.models.llm_cost import LLMCost
from typing import Optional, List, Dict

def apply_filters(query, realm_id: str, start_date: date, end_date: date, user_id: Optional[str] = None):
    query = query.filter(
        Usage.realm_id == realm_id,
        func.date(Usage.created_at) >= start_date,
        func.date(Usage.created_at) <= end_date
    )
    if user_id:
        query = query.filter(Usage.user_id == user_id)
    return query

def get_daily_costs(db: Session, realm_id: str, start_date: date, end_date: date, user_id: Optional[str] = None) -> List[Dict]:
    query = db.query(
        func.date(Usage.created_at).label('date'),
        LLMCost.provider_name,
        LLMCost.llm_model_name,
        func.sum(Usage.total_price).label('total_cost')
    ).join(LLMCost, Usage.llm_cost_id == LLMCost.id)
    
    query = apply_filters(query, realm_id, start_date, end_date, user_id)
    
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

def get_total_cost(db: Session, realm_id: str, start_date: date, end_date: date, user_id: Optional[str] = None) -> float:
    query = db.query(func.sum(Usage.total_model_price).label('total_cost'))
    query = apply_filters(query, realm_id, start_date, end_date, user_id)
    result = query.scalar()
    return float(result) if result else 0.0

def get_total_usage_fees(db: Session, realm_id: str, start_date: date, end_date: date, user_id: Optional[str] = None) -> float:
    query = db.query(
        (func.sum(Usage.total_price) - func.sum(Usage.total_model_price)).label('total_usage_fees')
    )
    query = apply_filters(query, realm_id, start_date, end_date, user_id)
    result = query.scalar()
    return float(result) if result else 0.0

def get_most_used_models(db: Session, realm_id: str, start_date: date, end_date: date, user_id: Optional[str] = None) -> List[Dict]:
    query = db.query(
        LLMCost.provider_name,
        LLMCost.llm_model_name,
        func.sum(Usage.total_tokens).label('total_tokens'),
        func.sum(Usage.total_model_price).label('total_model_price')
    ).join(LLMCost, Usage.llm_cost_id == LLMCost.id)
    
    query = apply_filters(query, realm_id, start_date, end_date, user_id)
    
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

def get_model_costs(db: Session, realm_id: str, start_date: date, end_date: date, user_id: Optional[str] = None) -> List[Dict]:
    query = db.query(
        LLMCost.provider_name,
        LLMCost.llm_model_name,
        func.date(Usage.created_at).label('date'),
        func.sum(Usage.total_model_price).label('daily_cost')
    ).join(LLMCost, Usage.llm_cost_id == LLMCost.id)
    
    query = apply_filters(query, realm_id, start_date, end_date, user_id)
    
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

def get_daily_tokens(db: Session, realm_id: str, start_date: date, end_date: date, user_id: Optional[str] = None):
    query = db.query(
        func.date(Usage.created_at).label('date'),
        func.sum(Usage.input_tokens).label('total_input_tokens'),
        func.sum(Usage.output_tokens).label('total_output_tokens')
    )

    query = apply_filters(query, realm_id, start_date, end_date, user_id)
    
    query = query.group_by(func.date(Usage.created_at)).order_by(func.date(Usage.created_at))

    results = query.all()

    return [
        {
            "date": str(result.date),
            "total_input_tokens": result.total_input_tokens,
            "total_output_tokens": result.total_output_tokens
        }
        for result in results
    ]

def get_model_daily_tokens(db: Session, realm_id: str, start_date: date, end_date: date, user_id: Optional[str] = None):
    query = db.query(
        func.date(Usage.created_at).label('date'),
        LLMCost.llm_model_name,
        func.sum(Usage.input_tokens).label('total_input_tokens'),
        func.sum(Usage.output_tokens).label('total_output_tokens')
    ).join(LLMCost, Usage.llm_cost_id == LLMCost.id)
    
    query = apply_filters(query, realm_id, start_date, end_date, user_id)
    
    query = query.group_by(func.date(Usage.created_at), LLMCost.llm_model_name).order_by(LLMCost.llm_model_name, func.date(Usage.created_at))

    results = query.all()

    model_data = {}
    for result in results:
        if result.llm_model_name not in model_data:
            model_data[result.llm_model_name] = {
                "llm_model_name": result.llm_model_name,
                "data": []
            }
        
        model_data[result.llm_model_name]["data"].append({
            "date": str(result.date),
            "total_input_tokens": result.total_input_tokens,
            "total_output_tokens": result.total_output_tokens
        })

    return list(model_data.values())

def get_top_users(db: Session, realm_id: str, start_date: date, end_date: date, limit: int = 10):
    # Get the total number of events for the given period and realm
    total_events = db.query(func.count(Usage.id)).filter(
        Usage.realm_id == realm_id,
        func.date(Usage.created_at) >= start_date,
        func.date(Usage.created_at) <= end_date
    ).scalar()

    # Get the top users with their activity counts for the specific realm
    results = db.query(
        Usage.user_id,
        func.count(Usage.id).label('total_activity_records')
    ).filter(
        Usage.realm_id == realm_id,
        func.date(Usage.created_at) >= start_date,
        func.date(Usage.created_at) <= end_date
    ).group_by(Usage.user_id).order_by(func.count(Usage.id).desc()).limit(limit).all()

    return {
        "total_events": total_events,
        "users": [
            {
                "user_id": result.user_id,
                "total_activity_records": result.total_activity_records,
                "percentage": (result.total_activity_records / total_events) * 100 if total_events > 0 else 0
            }
            for result in results
        ]
    }
