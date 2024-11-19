from yoyo import step

__depends__ = {'0016_refactor_llm_costs_table'}

steps = [
    step("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE api_logs (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            realm_id CHAR(24) NOT NULL,
            path VARCHAR(255) NOT NULL,
            method VARCHAR(10) NOT NULL,
            status_code INTEGER NOT NULL,
            origin VARCHAR(255),
            request_body JSONB,
            response_body JSONB,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (realm_id) REFERENCES realms(id) ON DELETE CASCADE
        );

        CREATE INDEX idx_api_logs_realm_id ON api_logs(realm_id);
        CREATE INDEX idx_api_logs_created_at ON api_logs(created_at);
    """,
    """
        DROP TABLE api_logs;
    """)
] 