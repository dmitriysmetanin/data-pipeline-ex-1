#!/bin/bash

echo "Waiting for Kafka Connect to start..."
while [ $(curl -s -o /dev/null -w %{http_code} http://localhost:8083/connectors) -ne 200 ]
do
  sleep 5
done

echo "Loading connector configuration from /etc/kafka-connect/config/postgres-connector.json"
CONNECTOR_NAME="debezium-postgres-connector"

# Always try to create the connector; if it exists, log the error
RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" --data @/etc/kafka-connect/config/postgres-connector.json http://localhost:8083/connectors)
HTTP_CODE=$?

if [ "$HTTP_CODE" = "0" ]; then
  if [[ "$RESPONSE" == *"already exists"* ]]; then
    echo "Connector $CONNECTOR_NAME already exists."
  else
    echo "Connector $CONNECTOR_NAME created successfully."
  fi
else
  echo "Failed to create connector. Response: $RESPONSE"
fi

echo "All connector configurations have been loaded!" 