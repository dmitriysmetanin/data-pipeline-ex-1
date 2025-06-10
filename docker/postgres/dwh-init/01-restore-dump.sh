#!/bin/bash
set -e

# Ждем, пока база данных будет готова
until pg_isready -U postgres; do
  echo "Waiting for postgres..."
  sleep 2
done

# Создаем базу данных, если она не существует
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'bank_dwh'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE bank_dwh"

# Восстанавливаем схему из 01-schema.sql
echo "Restoring database schema from 01-schema.sql..."
psql -U postgres -d bank_dwh -f /docker-entrypoint-initdb.d/01-schema.sql
echo "Database schema restore completed" 