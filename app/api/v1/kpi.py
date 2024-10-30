from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import kpi_service
from app.api.deps import get_current_user, check_realm_access
from datetime import date
from typing import Optional

router = APIRouter()

@router.get("/cost")
def get_kpi_cost(
    realm: dict = Depends(check_realm_access),
    start_date: date = Query(..., description="Start date for the KPI calculation"),
    end_date: date = Query(..., description="End date for the KPI calculation"),
    account_id: Optional[str] = Query(None, description="Optional account ID to filter results"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    daily_costs = kpi_service.get_daily_costs(db, realm.id, start_date, end_date, account_id)
    total_cost = kpi_service.get_total_cost(db, realm.id, start_date, end_date, account_id)
    total_usage_fees = kpi_service.get_total_usage_fees(db, realm.id, start_date, end_date, account_id)
    most_used_models = kpi_service.get_most_used_models(db, realm.id, start_date, end_date, account_id)
    model_costs = kpi_service.get_model_costs(db, realm.id, start_date, end_date, account_id)

    return {
        "daily_costs": daily_costs,
        "total_cost": total_cost,
        "total_usage_fees": total_usage_fees,
        "most_used_models": most_used_models,
        "model_costs": model_costs
    }

@router.get("/activity")
def get_kpi_activity(
    realm: dict = Depends(check_realm_access),
    start_date: date = Query(..., description="Start date for the KPI calculation"),
    end_date: date = Query(..., description="End date for the KPI calculation"),
    account_id: Optional[str] = Query(None, description="Optional account ID to filter results"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    daily_tokens = kpi_service.get_daily_tokens(db, realm.id, start_date, end_date, account_id)
    model_daily_tokens = kpi_service.get_model_daily_tokens(db, realm.id, start_date, end_date, account_id)
    top_users = kpi_service.get_top_users(db, realm.id, start_date, end_date)
    top_api_keys = kpi_service.get_top_api_keys(db, realm.id, start_date, end_date)

    return {
        "daily_tokens": daily_tokens,
        "model_daily_tokens": model_daily_tokens,
        "top_users": top_users,
        "top_api_keys": top_api_keys
    }
