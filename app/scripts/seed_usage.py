import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.models.usage import Usage
from app.models.llm_cost import LLMCost
from app.db.database import SessionLocal, engine
# from app.models import Base

def seed_usage_table(db: Session, num_records: int = 1000):
    # Ensure the database tables exist
    # Base.metadata.create_all(bind=engine)

    # Get the current time
    current_time = datetime.now(timezone.utc)

    # Get the time 3 months ago
    three_months_ago = current_time - timedelta(days=90)

    # Get the available LLM costs
    llm_costs = db.query(LLMCost).filter(LLMCost.id.in_([1, 2])).all()

    if not llm_costs:
        print("Error: No LLM costs found with id 1 or 2")
        return

    # Create and add usage records
    for _ in range(num_records):
        # Generate random data
        user_id = random.randint(1, 100)  # Assuming user IDs from 1 to 100
        llm_cost = random.choice(llm_costs)
        input_tokens = random.randint(10, 500)
        output_tokens = input_tokens + random.randint(10, 1000)
        total_tokens = input_tokens + output_tokens

        # Calculate prices
        price_per_token = llm_cost.price_per_unit / 1000 if llm_cost.unit_type == "1K" else llm_cost.price_per_unit
        total_model_price = total_tokens * price_per_token
        total_price = total_model_price * (1 + llm_cost.overhead / 100)

        # Generate a random timestamp within the last 3 months
        random_timestamp = three_months_ago + timedelta(
            seconds=random.randint(0, int((current_time - three_months_ago).total_seconds()))
        )

        # Create new usage record
        new_usage = Usage(
            user_id=f"user_{user_id}",
            llm_cost_id=llm_cost.id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            total_model_price=total_model_price,
            total_price=total_price,
            created_at=random_timestamp
        )

        db.add(new_usage)

    # Commit the changes
    try:
        db.commit()
        print(f"Successfully added {num_records} usage records.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while seeding usage data: {str(e)}")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_usage_table(db)
    finally:
        db.close()
