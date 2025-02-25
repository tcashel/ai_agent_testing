-- Create a read-only user for PostgreSQL

-- Create the readonly user
CREATE USER ${READONLY_USER} WITH PASSWORD '${READONLY_PASSWORD}';

-- Grant connect permissions
GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO ${READONLY_USER};

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO ${READONLY_USER};

-- Grant select permissions on all existing tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ${READONLY_USER};

-- Grant select permissions on all future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ${READONLY_USER};

-- Grant execute permissions on all functions
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO ${READONLY_USER};

-- Revoke any write permissions explicitly
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public FROM ${READONLY_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON TABLES FROM ${READONLY_USER};