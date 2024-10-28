from sqlalchemy.orm import Session
from app.models.llm_cost import LLMCost
from app.models.usage import Usage
from app.models.account import Account
from app.schemas.usage import UsageCreate
from datetime import datetime, timezone
from fastapi import HTTPException
import tiktoken
from uuid import UUID

def get_or_create_account(db: Session, external_id: str, realm_id: str) -> Account:
    account = db.query(Account).filter(
        Account.external_id == external_id,
        Account.realm_id == realm_id
    ).first()

    if not account:
        account = Account(
            external_id=external_id,
            realm_id=realm_id
        )
        db.add(account)
        db.commit()
        db.refresh(account)

    return account

def track_llm_usage(db: Session, usage: UsageCreate, api_key_id: UUID):
    current_time = datetime.now(timezone.utc)

    # Get the current LLM cost
    llm_cost = db.query(LLMCost).filter(
        LLMCost.provider_name == usage.provider_name,
        LLMCost.llm_model_name == usage.llm_model_name,
        LLMCost.valid_from <= current_time,
        (LLMCost.valid_to.is_(None) | (LLMCost.valid_to > current_time))
    ).order_by(LLMCost.valid_from.desc()).first()

    if not llm_cost:
        raise HTTPException(status_code=404, detail="LLM cost not found for the given provider and model")

    # Handle account lookup/creation if external_id is provided
    account_id = None
    if usage.external_id:
        account = get_or_create_account(db, usage.external_id, usage.realm_id)
        account_id = account.id

    # Tokenize message if provided
    if usage.message:
        encoding = tiktoken.encoding_for_model(usage.llm_model_name)
        tokens = encoding.encode(usage.message)
        usage.input_tokens = len(tokens)
        usage.output_tokens = 0

    # Calculate total tokens and prices
    total_tokens = usage.input_tokens + usage.output_tokens
    price_per_token = llm_cost.price_per_unit / 1000 if llm_cost.unit_type == "1K" else llm_cost.price_per_unit
    total_model_price = total_tokens * price_per_token
    total_price = total_model_price * (1 + llm_cost.overhead / 100)

    # Create new usage record
    new_usage = Usage(
        account_id=account_id,
        realm_id=usage.realm_id,
        api_key_id=api_key_id,
        llm_cost_id=llm_cost.id,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        total_tokens=total_tokens,
        total_model_price=total_model_price,
        total_price=total_price,
        created_at=current_time
    )

    db.add(new_usage)

    try:
        db.commit()
        return new_usage
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while tracking usage: {str(e)}")
