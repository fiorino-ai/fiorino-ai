from yoyo import step

__depends__ = {'0008_create_bill_limits_table'}

steps = [
    step("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE overheads (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            realm_id CHAR(24) NOT NULL,
            valid_from TIMESTAMP WITH TIME ZONE NOT NULL,
            valid_to TIMESTAMP WITH TIME ZONE,
            percentage FLOAT NOT NULL,
            FOREIGN KEY (realm_id) REFERENCES realms(id) ON DELETE CASCADE
        );

        CREATE INDEX idx_overheads_realm_id ON overheads(realm_id);
    """,
    """
        DROP TABLE overheads;
    """)
]
