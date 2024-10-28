from yoyo import step

__depends__ = {'0009_create_overheads_table'}

steps = [
    step("""
        ALTER TABLE usage
        ADD COLUMN api_key_id UUID,
        ADD CONSTRAINT fk_usage_api_key
        FOREIGN KEY (api_key_id)
        REFERENCES api_keys(id)
        ON DELETE SET NULL;

        CREATE INDEX idx_usage_api_key_id ON usage(api_key_id);
    """,
    """
        ALTER TABLE usage
        DROP CONSTRAINT fk_usage_api_key;

        DROP INDEX idx_usage_api_key_id;

        ALTER TABLE usage
        DROP COLUMN api_key_id;
    """)
]
