from yoyo import step

__depends__ = {'0001_create_llm_costs_table'}

steps = [
    step("""
        CREATE TABLE usage (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            llm_cost_id INTEGER NOT NULL,
            input_tokens INTEGER NOT NULL,
            output_tokens INTEGER NOT NULL,
            total_tokens INTEGER NOT NULL,
            total_model_price NUMERIC(10, 6) NOT NULL,
            total_price NUMERIC(10, 6) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            FOREIGN KEY (llm_cost_id) REFERENCES llm_costs (id)
        );

        CREATE INDEX idx_usage_user_id ON usage(user_id);
        CREATE INDEX idx_usage_created_at ON usage(created_at);
    """,
    """
        DROP TABLE usage
    """)
]
