from sqlalchemy.orm import Session
import string
import random
import getpass
from app.models.user import User
from app.db.database import SessionLocal
from app.core.security import get_password_hash
import re
import uuid

def generate_password(length=12):
    """Generate a random secure password"""
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        # Ensure password has at least one uppercase, one lowercase, one digit, and one special char
        if (any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(not c.isalnum() for c in password)):
            return password

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def create_user(db: Session, email: str, password: str):
    """Create a new user in the database"""
    # Hash the password using the same method as user_service
    hashed_password = get_password_hash(password)
    
    # Create user
    user = User(
        id=uuid.uuid4(),
        email=email,
        password_hash=hashed_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def main():
    print("\n=== Create New User ===\n")
    
    # Get email
    while True:
        email = input("Enter email address: ").strip()
        if is_valid_email(email):
            break
        print("Invalid email format. Please try again.")

    # Generate password
    password = generate_password()

    # Create user in database
    db = SessionLocal()
    try:
        user = create_user(db, email, password)
        print("\nUser created successfully!")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print("\nPlease save this password securely - it won't be shown again.")
        
    except Exception as e:
        print(f"\nError creating user: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 