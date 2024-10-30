import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.models import Usage, LLMCost, User, Realm, APIKey, Account
from app.db.database import SessionLocal, engine
import uuid
import hashlib
import time

def generate_api_key():
    plain_key = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(48))
    hashed_key = hashlib.sha256(plain_key.encode()).hexdigest()
    masked = '*' * 43 + plain_key[-5:]
    return hashed_key, masked

def seed_usage_table(db: Session, num_records: int = 10000):
    # Get the first user
    first_user = db.query(User).first()
    if not first_user:
        print("Error: No users found in the database")
        return

    # Create two realms for the user
    realm1 = Realm(name="Realm 1", created_by=first_user.id)
    realm2 = Realm(name="Realm 2", created_by=first_user.id)
    db.add(realm1)
    db.add(realm2)
    db.commit()
    db.refresh(realm1)
    db.refresh(realm2)

    # Create API keys for realms
    api_keys = []
    
    # Two API keys for realm1
    for i in range(2):
        hashed_key, masked = generate_api_key()
        api_key = APIKey(
            user_id=first_user.id,
            realm_id=realm1.id,
            name=f"API Key {i+1} - Realm 1",
            value=hashed_key,
            masked=masked
        )
        db.add(api_key)
        api_keys.append(api_key)

    # One API key for realm2
    hashed_key, masked = generate_api_key()
    api_key = APIKey(
        user_id=first_user.id,
        realm_id=realm2.id,
        name="API Key 1 - Realm 2",
        value=hashed_key,
        masked=masked
    )
    db.add(api_key)
    api_keys.append(api_key)
    
    db.commit()
    for key in api_keys:
        db.refresh(key)

    # Create random accounts for each realm
    accounts = []
    num_accounts = random.randint(30, 100)
    
    for i in range(num_accounts):
        realm = random.choice([realm1, realm2])
        account = Account(
            external_id=f"account_{i+1}",
            realm_id=realm.id,
            data={"seed_data": f"Account {i+1} data"}
        )
        db.add(account)
        accounts.append(account)
    
    db.commit()
    for account in accounts:
        db.refresh(account)

    # Group API keys by realm
    realm1_keys = [key for key in api_keys if key.realm_id == realm1.id]
    realm2_keys = [key for key in api_keys if key.realm_id == realm2.id]
    realm_api_keys = {
        realm1.id: realm1_keys,
        realm2.id: realm2_keys
    }

    # Group accounts by realm
    realm_accounts = {
        realm1.id: [acc for acc in accounts if acc.realm_id == realm1.id],
        realm2.id: [acc for acc in accounts if acc.realm_id == realm2.id]
    }

    # Get the current time and three months ago
    current_time = datetime.now(timezone.utc)
    three_months_ago = current_time - timedelta(days=90)

    # Get the available LLM costs
    llm_costs = db.query(LLMCost).filter(LLMCost.id.in_([1, 2])).all()
    if not llm_costs:
        print("Error: No LLM costs found with id 1 or 2")
        return

    # Create and add usage records
    for i in range(num_records):
        # Choose a random realm
        realm = random.choice([realm1, realm2])
        
        # Choose a random API key for the realm
        api_key = random.choice(realm_api_keys[realm.id])
        
        # Choose a random account for the realm
        account = random.choice(realm_accounts[realm.id]) if realm_accounts[realm.id] else None
        
        # Generate random data
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
            account_id=account.id if account else None,
            realm_id=realm.id,
            api_key_id=api_key.id,
            llm_cost_id=llm_cost.id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            total_model_price=total_model_price,
            total_price=total_price,
            created_at=random_timestamp
        )

        db.add(new_usage)

        # Every 500 entries, commit and wait
        if (i + 1) % 500 == 0:
            db.commit()
            wait_time = random.randint(100, 1500) / 1000  # Convert to seconds
            print(f"Processed {i + 1} records. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

    # Commit any remaining records
    try:
        db.commit()
        print(f"Successfully added {num_records} usage records.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while seeding usage data: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_usage_table(db)
    except Exception as e:
        print(f"An error occurred while seeding usage data: {str(e)}")
    finally:
        db.close()
