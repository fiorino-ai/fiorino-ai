from app.services import usage_service, api_key_service, api_log_service
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.usage import UsageCreate, UsageResponse
from app.api.deps import get_api_key
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/track")
async def track_usage(
    request: Request,
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
        tracked_usage = usage_service.track_llm_usage(db, usage, api_key_data.id)
        
        # Convert the tracked_usage to a response model
        usage_response = UsageResponse.model_validate(tracked_usage)
        response_data = {
            "message": "Usage tracked successfully",
            "usage": jsonable_encoder(usage_response)
        }

        # Log the API request
        await api_log_service.log_api_request(
            db=db,
            request=request,
            response=Response(),
            realm_id=api_key_data.realm_id,
            status_code=200,
            response_body=response_data
        )

        return response_data
    except HTTPException as e:
        # Log failed requests too
        if 'api_key_data' in locals():
            await api_log_service.log_api_request(
                db=db,
                request=request,
                response=Response(),
                realm_id=api_key_data.realm_id,
                status_code=e.status_code,
                response_body={"detail": e.detail}
            )
        raise e
    except Exception as e:
        # Log unexpected errors
        if 'api_key_data' in locals():
            await api_log_service.log_api_request(
                db=db,
                request=request,
                response=Response(),
                realm_id=api_key_data.realm_id,
                status_code=500,
                response_body={"detail": str(e)}
            )
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
