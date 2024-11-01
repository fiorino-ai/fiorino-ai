from yoyo import step

__depends__ = {'0014_alter_usage_table_llm_cost_uuid'}

steps = [
    step("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE large_language_models (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            realm_id CHAR(24) NOT NULL,
            provider_name VARCHAR(255) NOT NULL,
            model_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (realm_id) REFERENCES realms(id) ON DELETE CASCADE,
            UNIQUE(realm_id, provider_name, model_name)
        );

        CREATE INDEX idx_llm_realm_id ON large_language_models(realm_id);
        CREATE INDEX idx_llm_provider_model ON large_language_models(provider_name, model_name);
    """,
    """
        DROP TABLE large_language_models;
    """)
] 