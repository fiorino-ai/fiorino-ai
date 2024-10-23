from yoyo import step

__depends__ = {'0005_create_api_key_table'}

steps = [
    step("""
        ALTER TABLE usage
        ADD COLUMN realm_id CHAR(24);

        ALTER TABLE usage
        ADD CONSTRAINT fk_usage_realm
        FOREIGN KEY (realm_id)
        REFERENCES realms(id)
        ON DELETE CASCADE;

        CREATE INDEX idx_usage_realm_id ON usage(realm_id);
    """,
    """
        ALTER TABLE usage
        DROP CONSTRAINT fk_usage_realm;

        DROP INDEX idx_usage_realm_id;

        ALTER TABLE usage
        DROP COLUMN realm_id;
    """)
]
