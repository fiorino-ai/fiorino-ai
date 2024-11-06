from fastapi import APIRouter
from .llm_costs import router as llm_costs_router
from .usage import router as usage_router
from .kpi import router as kpi_router
from .auth import router as auth_router
from .realm import router as realm_router
from .api_key import router as api_key_router
from .bill_limit import router as bill_limit_router
from .overhead import router as overhead_router
from .account import router as account_router
from .api_log import router as api_log_router

v1_router = APIRouter()
v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
v1_router.include_router(usage_router, prefix="/usage", tags=["Usage"])
v1_router.include_router(realm_router, prefix="/realms", tags=["Realms"])
v1_router.include_router(kpi_router, prefix="/realms/{realm_id}/usage", tags=["KPI"])
v1_router.include_router(llm_costs_router, prefix="/realms/{realm_id}/llm-costs", tags=["LLM Costs"])
v1_router.include_router(api_key_router, prefix="/realms/{realm_id}/api-keys", tags=["API Keys"])
v1_router.include_router(bill_limit_router, prefix="/realms/{realm_id}/bill-limits", tags=["Bill Limits"])
v1_router.include_router(overhead_router, prefix="/realms/{realm_id}/overheads", tags=["Overheads"])
v1_router.include_router(account_router, prefix="/realms/{realm_id}/accounts", tags=["Accounts"])
v1_router.include_router(api_log_router, prefix="/realms/{realm_id}/usage", tags=["API Logs"])
