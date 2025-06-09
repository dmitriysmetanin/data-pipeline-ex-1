-- Создаем пользователя для Debezium
CREATE USER debezium WITH REPLICATION ENCRYPTED PASSWORD 'debezium';

-- Даем права на чтение всех таблиц в схеме public
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;

-- Даем права на чтение всех последовательностей в схеме public
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO debezium;

-- Даем права на чтение всех будущих таблиц в схеме public
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO debezium;

-- Даем права на чтение всех будущих последовательностей в схеме public
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO debezium;

-- Создаем публикацию для всех таблиц
CREATE PUBLICATION debezium_pub FOR ALL TABLES;

-- Включаем логическую репликацию
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET max_replication_slots = 10; 