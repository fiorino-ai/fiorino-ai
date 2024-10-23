from app.services import usage_service, api_key_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.usage import UsageCreate
from app.api.deps import get_api_key

router = APIRouter()

@router.post("/track")
async def track_usage(
    usage: UsageCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    try:
        # Validate API key and get associated realm
        api_key_data = api_key_service.validate_api_key(db, api_key)
        if not api_key_data:
            raise HTTPException(status_code=401, detail="Invalid or disabled API key")

        # Add realm_id to the usage data
        usage.realm_id = api_key_data.realm_id

        # Track the usage
        tracked_usage = usage_service.track_llm_usage(db, usage)
        return {"message": "Usage tracked successfully", "usage": tracked_usage}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
