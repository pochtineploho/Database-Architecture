#!/bin/bash

# Определение переменной окружения для версии миграции
MIGRATION_VERSION=${MIGRATION_VERSION:-latest}

# Если версия миграции указана как "latest", найдем последнюю версию
if [ "$MIGRATION_VERSION" == "latest" ]; then
    LATEST_VERSION=$(ls -1 /migrations | grep -E "^[0-9]+\.[0-9]+\.sql$" | sort -V | tail -n1)
    if [ -n "$LATEST_VERSION" ]; then
        MIGRATION_VERSION=$LATEST_VERSION
    else
        echo "Не найдено миграций"
        exit 1
    fi
fi

# Выполнение всех миграций до указанной версии включительно
for migration_file in $(ls -1 /migrations | grep -E "^[0-9]+\.[0-9]+\.sql$" | sort -V); do
    if [ "$(basename "$migration_file")" \> "$MIGRATION_VERSION" ]; then
        break
    fi
    psql -U postgres -d flowwow -f "/migrations/$migration_file"
done