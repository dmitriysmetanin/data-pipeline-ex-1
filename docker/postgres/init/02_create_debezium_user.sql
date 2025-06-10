-- Create debezium user with replication privilege
CREATE USER debezium WITH REPLICATION ENCRYPTED PASSWORD 'dbz';

-- Grant permissions to debezium user
GRANT CONNECT ON DATABASE bank_oltp2 TO debezium;
GRANT USAGE ON SCHEMA public TO debezium;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO debezium;

-- Grant permissions for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO debezium;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON SEQUENCES TO debezium;

-- Grant superuser privileges temporarily to create publication
ALTER USER debezium WITH SUPERUSER; 