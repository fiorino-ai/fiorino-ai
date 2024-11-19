from yoyo import step

__depends__ = {'0004_create_realm_table'}

steps = [
    step("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE api_keys (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID NOT NULL,
            realm_id CHAR(24) NOT NULL,
            name VARCHAR(255) NOT NULL,
            value VARCHAR(255) NOT NULL,
            masked VARCHAR(48) NOT NULL,
            is_disabled BOOLEAN NOT NULL DEFAULT FALSE,
            disabled_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (realm_id) REFERENCES realms(id) ON DELETE CASCADE
        );

        CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
        CREATE INDEX idx_api_keys_realm_id ON api_keys(realm_id);
        CREATE UNIQUE INDEX idx_api_keys_value ON api_keys(value);
        CREATE INDEX idx_api_keys_name ON api_keys(name);
    """,
    """
        DROP TABLE api_keys;
    """)
]
