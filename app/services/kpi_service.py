from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime, timezone
from app.models.usage import Usage
from app.models.llm_cost import LLMCost
from app.models.api_key import APIKey
from app.models.account import Account
from app.models.large_language_model import LargeLanguageModel
from app.models.bill_limit import BillLimit
from typing import Optional, List, Dict
from uuid import UUID

def apply_filters(query, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None):
    query = query.filter(
        Usage.realm_id == realm_id,
        func.date(Usage.created_at) >= start_date,
        func.date(Usage.created_at) <= end_date
    )
    if account_id:
        query = query.filter(Usage.account_id == account_id)
    return query

def get_daily_costs(db: Session, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None) -> List[Dict]:
    query = db.query(
        func.date(Usage.created_at).label('date'),
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name,
        func.sum(Usage.total_price).label('total_cost')
    ).join(
        LLMCost, Usage.llm_cost_id == LLMCost.id
    ).join(
        LargeLanguageModel, LLMCost.llm_id == LargeLanguageModel.id
    )
    
    query = apply_filters(query, realm_id, start_date, end_date, account_id)
    
    query = query.group_by(
        func.date(Usage.created_at),
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name
    ).order_by(func.date(Usage.created_at))
    
    results = query.all()
    
    return [
        {
            'date': result.date,
            'provider_name': result.provider_name,
            'model_name': result.model_name,
            'total_cost': float(result.total_cost)
        }
        for result in results
    ]

def get_total_cost(db: Session, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None) -> float:
    query = db.query(func.sum(Usage.total_model_price).label('total_cost'))
    query = apply_filters(query, realm_id, start_date, end_date, account_id)
    result = query.scalar()
    return float(result) if result else 0.0

def get_total_usage_fees(db: Session, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None) -> float:
    query = db.query(
        (func.sum(Usage.total_price) - func.sum(Usage.total_model_price)).label('total_usage_fees')
    )
    query = apply_filters(query, realm_id, start_date, end_date, account_id)
    result = query.scalar()
    return float(result) if result else 0.0

def get_most_used_models(db: Session, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None) -> List[Dict]:
    query = db.query(
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name,
        func.sum(Usage.total_tokens).label('total_tokens'),
        func.sum(Usage.total_model_price).label('total_model_price')
    ).join(
        LLMCost, Usage.llm_cost_id == LLMCost.id
    ).join(
        LargeLanguageModel, LLMCost.llm_id == LargeLanguageModel.id
    )
    
    query = apply_filters(query, realm_id, start_date, end_date, account_id)
    
    query = query.group_by(
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name
    ).order_by(func.sum(Usage.total_tokens).desc())
    
    results = query.all()
    
    return [
        {
            'provider_name': result.provider_name,
            'model_name': result.model_name,
            'total_tokens': int(result.total_tokens),
            'total_model_price': float(result.total_model_price)
        }
        for result in results
    ]

def get_model_costs(db: Session, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None) -> List[Dict]:
    query = db.query(
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name,
        func.date(Usage.created_at).label('date'),
        func.sum(Usage.total_model_price).label('daily_cost')
    ).join(
        LLMCost, Usage.llm_cost_id == LLMCost.id
    ).join(
        LargeLanguageModel, LLMCost.llm_id == LargeLanguageModel.id
    )
    
    query = apply_filters(query, realm_id, start_date, end_date, account_id)
    
    query = query.group_by(
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name,
        func.date(Usage.created_at)
    ).order_by(
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name,
        func.date(Usage.created_at)
    )
    
    results = query.all()
    
    model_costs = {}
    for result in results:
        model_key = f"{result.provider_name}:{result.model_name}"
        if model_key not in model_costs:
            model_costs[model_key] = {
                'provider_name': result.provider_name,
                'model_name': result.model_name,
                'daily_costs': []
            }
        model_costs[model_key]['daily_costs'].append({
            'date': result.date,
            'cost': float(result.daily_cost)
        })
    
    return list(model_costs.values())

def get_daily_tokens(db: Session, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None):
    query = db.query(
        func.date(Usage.created_at).label('date'),
        func.sum(Usage.input_tokens).label('total_input_tokens'),
        func.sum(Usage.output_tokens).label('total_output_tokens')
    )

    query = apply_filters(query, realm_id, start_date, end_date, account_id)
    
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

def get_model_daily_tokens(db: Session, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None):
    query = db.query(
        func.date(Usage.created_at).label('date'),
        LargeLanguageModel.model_name,
        func.sum(Usage.input_tokens).label('total_input_tokens'),
        func.sum(Usage.output_tokens).label('total_output_tokens')
    ).join(
        LLMCost, Usage.llm_cost_id == LLMCost.id
    ).join(
        LargeLanguageModel, LLMCost.llm_id == LargeLanguageModel.id
    )
    
    query = apply_filters(query, realm_id, start_date, end_date, account_id)
    
    query = query.group_by(func.date(Usage.created_at), LargeLanguageModel.model_name).order_by(LargeLanguageModel.model_name, func.date(Usage.created_at))

    results = query.all()

    model_data = {}
    for result in results:
        if result.model_name not in model_data:
            model_data[result.model_name] = {
                "model_name": result.model_name,
                "data": []
            }
        
        model_data[result.model_name]["data"].append({
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
        func.date(Usage.created_at) <= end_date,
        Usage.account_id.isnot(None)  # Only count events with account_id
    ).scalar()

    # Get the top accounts with their activity counts for the specific realm
    results = db.query(
        Usage.account_id,
        Account.external_id.label('account_name'),
        func.count(Usage.id).label('total_activity_records')
    ).join(
        Account, Usage.account_id == Account.id
    ).filter(
        Usage.realm_id == realm_id,
        func.date(Usage.created_at) >= start_date,
        func.date(Usage.created_at) <= end_date,
        Usage.account_id.isnot(None)
    ).group_by(
        Usage.account_id,
        Account.external_id
    ).order_by(
        func.count(Usage.id).desc()
    ).limit(limit).all()

    return {
        "total_events": total_events,
        "users": [
            {
                "account_id": str(result.account_id),
                "account_name": result.account_name,
                "total_activity_records": result.total_activity_records,
                "percentage": (result.total_activity_records / total_events) * 100 if total_events > 0 else 0
            }
            for result in results
        ]
    }

def get_top_api_keys(db: Session, realm_id: str, start_date: date, end_date: date, limit: int = 10):
    # Get the total number of events for the given period and realm
    total_events = db.query(func.count(Usage.id)).filter(
        Usage.realm_id == realm_id,
        func.date(Usage.created_at) >= start_date,
        func.date(Usage.created_at) <= end_date,
        Usage.api_key_id.isnot(None)  # Only count events with api_key_id
    ).scalar()

    # Get the top API keys with their activity counts for the specific realm
    results = db.query(
        Usage.api_key_id,
        APIKey.name.label('api_key_name'),
        func.count(Usage.id).label('total_activity_records')
    ).join(
        APIKey, Usage.api_key_id == APIKey.id
    ).filter(
        Usage.realm_id == realm_id,
        func.date(Usage.created_at) >= start_date,
        func.date(Usage.created_at) <= end_date,
        Usage.api_key_id.isnot(None)
    ).group_by(
        Usage.api_key_id,
        APIKey.name
    ).order_by(
        func.count(Usage.id).desc()
    ).limit(limit).all()

    return {
        "total_events": total_events,
        "api_keys": [
            {
                "api_key_name": result.api_key_name,
                "total_activity_records": result.total_activity_records,
                "percentage": (result.total_activity_records / total_events) * 100 if total_events > 0 else 0
            }
            for result in results
        ]
    }

def get_used_llms(db: Session, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None) -> Dict:
    query = db.query(
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name
    ).join(
        LLMCost, LLMCost.llm_id == LargeLanguageModel.id
    ).join(
        Usage, Usage.llm_cost_id == LLMCost.id
    ).filter(
        Usage.realm_id == realm_id,
        func.date(Usage.created_at) >= start_date,
        func.date(Usage.created_at) <= end_date
    )

    if account_id:
        query = query.filter(Usage.account_id == account_id)

    query = query.group_by(
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name
    ).order_by(
        LargeLanguageModel.provider_name,
        LargeLanguageModel.model_name
    )

    results = query.all()

    return [
        {
            "provider_name": result.provider_name,
            "model_name": result.model_name
        }
        for result in results
    ]

def get_current_bill_limit(db: Session, realm_id: str, current_time: datetime) -> Optional[float]:
    """Get the current bill limit amount for a realm"""
    current_limit = (
        db.query(BillLimit)
        .filter(
            BillLimit.realm_id == realm_id,
            BillLimit.valid_from <= current_time,
            (BillLimit.valid_to.is_(None) | (BillLimit.valid_to > current_time))
        )
        .order_by(BillLimit.valid_from.desc())
        .first()
    )
    
    return current_limit.amount if current_limit else None

def get_kpi_cost(db: Session, realm_id: str, start_date: date, end_date: date, account_id: Optional[UUID] = None) -> dict:
    """Get cost KPIs including budget information"""
    daily_costs = get_daily_costs(db, realm_id, start_date, end_date, account_id)
    total_cost = get_total_cost(db, realm_id, start_date, end_date, account_id)
    total_usage_fees = get_total_usage_fees(db, realm_id, start_date, end_date, account_id)
    most_used_models = get_most_used_models(db, realm_id, start_date, end_date, account_id)
    model_costs = get_model_costs(db, realm_id, start_date, end_date, account_id)
    llms = get_used_llms(db, realm_id, start_date, end_date, account_id)
    
    # Get current bill limit
    current_time = datetime.now(timezone.utc)
    current_budget = get_current_bill_limit(db, realm_id, current_time)
    
    # Calculate budget usage percentage
    budget_usage_percentage = (
        (total_cost / current_budget) * 100 
        if current_budget and total_cost > 0 
        else 0
    )

    return {
        "daily_costs": daily_costs,
        "total_cost": total_cost,
        "total_usage_fees": total_usage_fees,
        "most_used_models": most_used_models,
        "model_costs": model_costs,
        "llms": llms,
        "budget": {
            "current_budget": current_budget,
            "budget_usage_percentage": round(budget_usage_percentage, 2)
        }
    }
