from yoyo import step
import uuid

__depends__ = {'0002_create_usage_table'}

steps = [
    step("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            reset_password_token VARCHAR(255),
            reset_password_token_expiry TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX idx_users_email ON users(email);
    """,
    """
        DROP TABLE users;
        DROP EXTENSION IF EXISTS "uuid-ossp";
    """)
]
