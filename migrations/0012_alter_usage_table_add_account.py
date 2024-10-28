from yoyo import step

__depends__ = {'0011_create_accounts_table'}

steps = [
    step("""
        -- Add new column and foreign key
        ALTER TABLE usage
        ADD COLUMN account_id UUID,
        ADD CONSTRAINT fk_usage_account
        FOREIGN KEY (account_id)
        REFERENCES accounts(id)
        ON DELETE SET NULL;

        -- Create index for the new column
        CREATE INDEX idx_usage_account_id ON usage(account_id);

        -- Drop the old user_id column
        ALTER TABLE usage
        DROP COLUMN user_id;
    """,
    """
        -- Revert changes
        ALTER TABLE usage
        ADD COLUMN user_id VARCHAR(255);

        ALTER TABLE usage
        DROP CONSTRAINT fk_usage_account;

        DROP INDEX idx_usage_account_id;

        ALTER TABLE usage
        DROP COLUMN account_id;
    """)
] 