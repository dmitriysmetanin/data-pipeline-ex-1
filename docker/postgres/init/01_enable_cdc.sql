-- Включаем логическую репликацию
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_wal_senders = 1;
ALTER SYSTEM SET max_replication_slots = 1;

-- Создаем пользователя для репликации
CREATE USER debezium WITH REPLICATION ENCRYPTED PASSWORD 'dbz';

-- Даем права на все таблицы
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO debezium; 