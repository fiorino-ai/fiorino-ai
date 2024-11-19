from yoyo import step

__depends__ = {'0012_alter_usage_table_add_account'}

steps = [
    step("""
        -- Create temporary table with new structure
        CREATE TABLE llm_costs_new (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            provider_name VARCHAR(255) NOT NULL,
            llm_model_name VARCHAR(255) NOT NULL,
            price_per_unit FLOAT NOT NULL,
            unit_type VARCHAR(20) NOT NULL,
            overhead FLOAT DEFAULT 0,
            valid_from TIMESTAMP NOT NULL,
            valid_to TIMESTAMP,
            is_system BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (provider_name, llm_model_name)
        );

        -- Copy data from old table to new table
        INSERT INTO llm_costs_new (
            id,
            provider_name,
            llm_model_name,
            price_per_unit,
            unit_type,
            overhead,
            valid_from,
            valid_to,
            is_system,
            created_at,
            updated_at
        )
        SELECT 
            uuid_generate_v4(),
            provider_name,
            llm_model_name,
            price_per_unit,
            unit_type,
            overhead,
            valid_from,
            valid_to,
            is_system,
            created_at,
            updated_at
        FROM llm_costs;

        -- Update foreign key references in usage table
        ALTER TABLE usage DROP CONSTRAINT usage_llm_cost_id_fkey;
        
        -- Drop old table and rename new table
        DROP TABLE llm_costs;
        ALTER TABLE llm_costs_new RENAME TO llm_costs;

        -- Recreate indexes
        CREATE INDEX idx_valid_period ON llm_costs(valid_from, valid_to);
        CREATE INDEX idx_provider_model_valid_period ON llm_costs(provider_name, llm_model_name, valid_from, valid_to);
    """,
    """
        -- Revert changes (if needed)
        CREATE TABLE llm_costs_old (
            id SERIAL PRIMARY KEY,
            provider_name VARCHAR(255) NOT NULL,
            llm_model_name VARCHAR(255) NOT NULL,
            price_per_unit FLOAT NOT NULL,
            unit_type VARCHAR(20) NOT NULL,
            overhead FLOAT DEFAULT 0,
            valid_from TIMESTAMP NOT NULL,
            valid_to TIMESTAMP,
            is_system BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (provider_name, llm_model_name)
        );

        DROP TABLE llm_costs;
        ALTER TABLE llm_costs_old RENAME TO llm_costs;
    """)
] 