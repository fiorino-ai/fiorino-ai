from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE llm_costs (
            id SERIAL PRIMARY KEY,
            provider_name VARCHAR(255) NOT NULL,
            model_name VARCHAR(255) NOT NULL,
            price_per_unit FLOAT NOT NULL,
            unit_type VARCHAR(20) NOT NULL,
            overhead FLOAT DEFAULT 0,
            valid_from TIMESTAMP NOT NULL,
            valid_to TIMESTAMP,
            is_system BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (provider_name, model_name)
        );

        CREATE INDEX idx_valid_period ON llm_costs(valid_from, valid_to);
    """,
    "DROP TABLE llm_costs")
]
