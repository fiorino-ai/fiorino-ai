from yoyo import step

__depends__ = {'0006_add_realm_id_to_usage_table'}

steps = [
    step("""
        ALTER TABLE realms
        ADD COLUMN bill_limit_enabled BOOLEAN NOT NULL DEFAULT FALSE,
        ADD COLUMN overhead_enabled BOOLEAN NOT NULL DEFAULT FALSE;
    """,
    """
        ALTER TABLE realms
        DROP COLUMN bill_limit_enabled,
        DROP COLUMN overhead_enabled;
    """)
]
