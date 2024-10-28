from yoyo import step

__depends__ = {'0010_add_api_key_to_usage_table'}

steps = [
    step("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE accounts (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            external_id VARCHAR(255) NOT NULL,
            data JSONB,
            realm_id CHAR(24) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (realm_id) REFERENCES realms(id) ON DELETE CASCADE
        );

        CREATE INDEX idx_accounts_realm_id ON accounts(realm_id);
        CREATE INDEX idx_accounts_external_id ON accounts(external_id);
        CREATE INDEX idx_accounts_data ON accounts USING gin (data);
    """,
    """
        DROP TABLE accounts;
    """)
] 