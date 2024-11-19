from yoyo import step

__depends__ = {'0003_create_users_table'}

steps = [
    step("""
        -- Function to generate a random 24-character string
        CREATE OR REPLACE FUNCTION generate_object_id() 
        RETURNS char(24) AS $$
        DECLARE
            time_component char(8);
            machine_id char(6);
            process_id char(4);
            counter char(6);
        BEGIN
            -- Time component: 4-byte timestamp
            time_component := lpad(to_hex(extract(epoch from now())::integer), 8, '0');
            
            -- Machine ID: 3-byte random
            machine_id := lpad(to_hex((random()*16777215)::integer), 6, '0');
            
            -- Process ID: 2-byte random
            process_id := lpad(to_hex((random()*65535)::integer), 4, '0');
            
            -- Counter: 3-byte random
            counter := lpad(to_hex((random()*16777215)::integer), 6, '0');
            
            RETURN time_component || machine_id || process_id || counter;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TABLE realms (
            id char(24) PRIMARY KEY DEFAULT generate_object_id(),
            name VARCHAR(255) NOT NULL,
            created_by UUID NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        );

        CREATE INDEX idx_realms_name ON realms(name);
        CREATE INDEX idx_realms_created_by ON realms(created_by);
    """,
    """
        DROP TABLE realms;
        DROP FUNCTION IF EXISTS generate_object_id();
    """)
]
