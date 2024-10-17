from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.usage import UsageCreate
from app.services.usage_service import track_llm_usage

router = APIRouter()

@router.post("/track")
async def track_usage(usage: UsageCreate, db: Session = Depends(get_db)):
    try:
        tracked_usage = track_llm_usage(db, usage)
        return {"message": "Usage tracked successfully", "usage": tracked_usage}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
