from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services import kpi_service
from app.api.deps import get_current_user, check_realm_access
from datetime import date, datetime, timezone
from typing import Optional
from uuid import UUID

router = APIRouter()

@router.get("/cost")
def get_kpi_cost(
    realm: dict = Depends(check_realm_access),
    start_date: date = Query(..., description="Start date for the KPI calculation"),
    end_date: date = Query(..., description="End date for the KPI calculation"),
    account_id: Optional[UUID] = Query(None, description="Optional account ID to filter results"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get cost KPIs including:
    - Daily costs
    - Total cost
    - Usage fees
    - Most used models
    - Model costs
    - Current budget and usage percentage
    """
    return kpi_service.get_kpi_cost(db, realm.id, start_date, end_date, account_id)

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
