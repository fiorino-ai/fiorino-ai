from yoyo import step

__depends__ = {'0007_add_bill_limit_and_overhead_to_realm'}

steps = [
    step("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE bill_limits (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            realm_id CHAR(24) NOT NULL,
            valid_from TIMESTAMP WITH TIME ZONE NOT NULL,
            valid_to TIMESTAMP WITH TIME ZONE,
            amount FLOAT NOT NULL,
            FOREIGN KEY (realm_id) REFERENCES realms(id) ON DELETE CASCADE
        );

        CREATE INDEX idx_bill_limits_realm_id ON bill_limits(realm_id);
    """,
    """
        DROP TABLE bill_limits;
    """)
]
