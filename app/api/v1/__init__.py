from fastapi import APIRouter
from .llm_costs import router as llm_costs_router
from .usage import router as usage_router
from .kpi import router as kpi_router
from .auth import router as auth_router

v1_router = APIRouter()
v1_router.include_router(llm_costs_router, prefix="/llm-costs", tags=["LLM Costs"])
v1_router.include_router(usage_router, prefix="/usage", tags=["Usage"])
v1_router.include_router(kpi_router, prefix="/kpi", tags=["KPI"])
v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
