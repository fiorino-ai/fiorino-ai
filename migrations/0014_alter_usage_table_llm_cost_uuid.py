from yoyo import step

__depends__ = {'0013_alter_llm_costs_table_uuid'}

steps = [
    step("""
        -- Add new UUID column
        ALTER TABLE usage
        ADD COLUMN llm_cost_id_new UUID;

        -- Update the new column with corresponding UUID values from llm_costs
        UPDATE usage u
        SET llm_cost_id_new = lc.id
        FROM llm_costs lc
        WHERE u.llm_cost_id = lc.id::text::integer;

        -- Drop the old column and rename the new one
        ALTER TABLE usage
        DROP COLUMN llm_cost_id;

        ALTER TABLE usage
        RENAME COLUMN llm_cost_id_new TO llm_cost_id;

        -- Add NOT NULL constraint and foreign key
        ALTER TABLE usage
        ALTER COLUMN llm_cost_id SET NOT NULL;

        ALTER TABLE usage
        ADD CONSTRAINT fk_usage_llm_cost
        FOREIGN KEY (llm_cost_id)
        REFERENCES llm_costs(id);

        -- Create index for the new column
        CREATE INDEX idx_usage_llm_cost_id ON usage(llm_cost_id);
    """,
    """
        -- Revert changes
        ALTER TABLE usage
        DROP CONSTRAINT fk_usage_llm_cost;

        DROP INDEX idx_usage_llm_cost_id;

        ALTER TABLE usage
        ADD COLUMN llm_cost_id_old INTEGER;

        UPDATE usage u
        SET llm_cost_id_old = llm_cost_id::text::integer;

        ALTER TABLE usage
        DROP COLUMN llm_cost_id;

        ALTER TABLE usage
        RENAME COLUMN llm_cost_id_old TO llm_cost_id;

        ALTER TABLE usage
        ALTER COLUMN llm_cost_id SET NOT NULL;
    """)
] 