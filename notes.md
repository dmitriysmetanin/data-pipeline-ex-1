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

### Посмотреть список топиков
docker exec -it itis-architecture-kafka-1 kafka-topics --bootstrap-server localhost:9092 --list

### Подписаться на конкретный топик
<p>topic_name: имя топика</p>
<p>docker exec -it itis-architecture-kafka-1 kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver1.public.*topic_name* --from-beginning --property print.key=true</p>
