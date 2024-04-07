#!/bin/bash

# Определение переменной окружения для версии миграции
MIGRATION_VERSION=${MIGRATION_VERSION:-latest}

# Выполнение миграций в зависимости от версии
if [ "$MIGRATION_VERSION" == "latest" ]; then
    # Выполнить все миграции
    for migration_script in /migrations/*.sql; do
        psql -U postgres -d flowwow -f "$migration_script"
    done
else
    # Выполнить миграции до указанной версии
    for migration_script in /migrations/V*.sql; do
        version=$(basename "$migration_script" .sql | sed 's/^V//')
        if ! [ "$version" \> "$MIGRATION_VERSION" ]; then
            psql -U postgres -d flowwow -f "$migration_script"
        fi
    done
fi
