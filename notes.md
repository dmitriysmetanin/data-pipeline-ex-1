## Важные заметки для проекта

2025-09-06 20:02
Пока что не настроил создание коннектора после старта kafka-connect. 
Необходимо вручную прописывать

curl -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d '
{
  "name": "debezium-postgres-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "app-db",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "dbz",
    "database.dbname": "bank_oltp2",
    "database.server.name": "dbserver1",
    "topic.prefix": "dbserver1",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot",
    "publication.name": "debezium_pub",
    "table.include.list": "public.*",
    "tombstones.on.delete": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter"
  }
}'
