from yoyo import step

__depends__ = {'0015_create_large_language_models_table'}

steps = [
    step("""
        -- Create temporary table with new structure
        CREATE TABLE llm_costs_new (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            llm_id UUID NOT NULL,
            realm_id CHAR(24) NOT NULL,
            price_per_unit FLOAT NOT NULL,
            unit_type VARCHAR(20) NOT NULL,
            overhead FLOAT DEFAULT 0,
            valid_from TIMESTAMP WITH TIME ZONE NOT NULL,
            valid_to TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (llm_id) REFERENCES large_language_models(id) ON DELETE CASCADE,
            FOREIGN KEY (realm_id) REFERENCES realms(id) ON DELETE CASCADE
        );

        -- Update foreign key references in usage table
        ALTER TABLE usage DROP CONSTRAINT fk_usage_llm_cost;
        
        -- Drop old table and rename new table
        DROP TABLE llm_costs;
        ALTER TABLE llm_costs_new RENAME TO llm_costs;

        -- Recreate indexes and constraints
        CREATE INDEX idx_llm_costs_realm_id ON llm_costs(realm_id);
        CREATE INDEX idx_llm_costs_llm_id ON llm_costs(llm_id);
        CREATE INDEX idx_llm_costs_valid_period ON llm_costs(valid_from, valid_to);

        -- Recreate foreign key from usage table
        ALTER TABLE usage
        ADD CONSTRAINT fk_usage_llm_cost
        FOREIGN KEY (llm_cost_id)
        REFERENCES llm_costs(id);
    """,
    """
        -- Revert changes
        CREATE TABLE llm_costs_old (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            provider_name VARCHAR(255) NOT NULL,
            llm_model_name VARCHAR(255) NOT NULL,
            price_per_unit FLOAT NOT NULL,
            unit_type VARCHAR(20) NOT NULL,
            overhead FLOAT DEFAULT 0,
            valid_from TIMESTAMP WITH TIME ZONE NOT NULL,
            valid_to TIMESTAMP WITH TIME ZONE,
            is_system BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (provider_name, llm_model_name)
        );

        -- Drop new table and rename old table back
        DROP TABLE llm_costs;
        ALTER TABLE llm_costs_old RENAME TO llm_costs;
    """)
] 