-- Grant necessary permissions to the database user

-- Connect to the database as a superuser (postgres)
-- Run these commands as a superuser:

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO harsh;

-- Grant all privileges on all tables in the schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO harsh;

-- Grant privileges on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO harsh;

-- Grant privileges on sequences
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO harsh;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO harsh;

-- Make harsh the owner of the schema (optional, only if needed)
-- ALTER SCHEMA public OWNER TO harsh;
