-- Создаем пользователя debezium
CREATE USER debezium WITH REPLICATION ENCRYPTED PASSWORD 'dbz';

-- Даем права на все таблицы в схеме public
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO debezium;

-- Включаем логическую репликацию
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET max_replication_slots = 10; 